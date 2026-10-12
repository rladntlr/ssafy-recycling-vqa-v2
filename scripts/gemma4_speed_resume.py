"""Colab: stop cell 8, run this file in the SAME runtime, then rerun cell 8."""
import inspect
import time
import textwrap
import copy
import datetime
import ast

_speed_required = ['generate_vote', 'common_manifest', 'OUT_DIR', 'PRESET', 'RUN_MODE',
                   'atomic_json', 'function_names', 'code_signature', 'dino_manifest']
_missing = [k for k in _speed_required if k not in globals()]
if _missing:
    raise RuntimeError(f"기존 실행 런타임에서 8번만 중단한 뒤 실행하세요. 누락: {_missing}")
if RUN_MODE != 'test' or MODEL_ID != 'google/gemma-4-31B-it':
    raise RuntimeError('이 패치는 현재 Gemma 4 테스트 실행용입니다.')
if globals().get('_gemma_speed_applied'):
    print('이미 적용되어 있습니다. 8번 셀만 다시 실행하세요.')
else:
    _folder = OUT_DIR / PRESET
    _manifest_path = _folder / 'run_config.json'
    _old_manifest = json.loads(_manifest_path.read_text(encoding='utf-8'))
    if _old_manifest != dict(common_manifest, preset=PRESET):
        raise RuntimeError('메모리 설정과 기존 체크포인트 설정이 다릅니다. 기존 설정을 먼저 확인하세요.')

    # Use this runtime's actual function, preserving any current prompt/generation choices.
    _original_vote = generate_vote
    _fn = generate_vote
    while hasattr(_fn, '__wrapped__'):
        _fn = _fn.__wrapped__
    try:
        _source = textwrap.dedent(inspect.getsource(_fn))
    except (OSError, TypeError) as exc:
        raise RuntimeError('현재 추론 함수 소스를 읽지 못했습니다. 패치를 적용하지 않았습니다.') from exc
    _cleanup = '            gc.collect()\n            torch.cuda.empty_cache()'
    if _cleanup not in _source or '        except torch.cuda.OutOfMemoryError:\n' not in _source:
        raise RuntimeError('예상한 메모리 정리 구조가 아닙니다. 패치를 적용하지 않았습니다.')
    _source = _source.replace('        views = inputs = outputs = None',
        '        views = inputs = outputs = None\n        cleanup_needed = False\n        vote_started = time.perf_counter()')
    _source = _source.replace('        except torch.cuda.OutOfMemoryError:\n',
        '        except torch.cuda.OutOfMemoryError:\n            cleanup_needed = True\n')
    _source = _source.replace(_cleanup,
        '            if cleanup_needed:\n                gc.collect()\n                torch.cuda.empty_cache()')
    _source = _source.replace('max_soft_tokens=image_tokens).to(model.device)',
        'processor_kwargs={"max_soft_tokens": image_tokens}).to(model.device)')
    _source = _source.replace('            budget = THINK_TOKENS',
        '            preprocessing_seconds = time.perf_counter() - vote_started\n            generation_started = time.perf_counter()\n            budget = THINK_TOKENS')
    _source = _source.replace('            displayed = parse_answer(raw, thinking)',
        '            generation_seconds = time.perf_counter() - generation_started\n            displayed = parse_answer(raw, thinking)')
    _source = _source.replace('return dict(answer=original_label(displayed, order), raw=raw,',
        'return dict(answer=original_label(displayed, order), raw=raw,\n'
        '                speed_patch="gpu-dino-cleanup-v1", preprocessing_seconds=preprocessing_seconds,\n'
        '                generation_seconds=generation_seconds,')
    ast.parse(_source)
    _isolated = {}
    exec(compile(_source, '<gemma_speed_vote>', 'exec'), globals(), _isolated)
    _new_vote = _isolated['generate_vote']
    _old_dino_device = DINO_DEVICE
    _stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    _saved_items = sorted(p.name for p in (_folder / 'items').glob('*.json'))
    _new_common = copy.deepcopy(common_manifest)
    _new_dino_manifest = copy.deepcopy(dino_manifest)
    _target_device = str(model.device)
    if CROP_BACKEND == 'dinov3':
        gc.collect()
        torch.cuda.empty_cache()
        _free, _ = torch.cuda.mem_get_info(model.device)
        _weights = sum(p.numel() * p.element_size() for p in dino_model.parameters())
        if _free < _weights + 6 * 2**30:
            raise RuntimeError('DINO GPU 이동용 여유 메모리가 부족합니다. 현재 실행은 변경하지 않았습니다.')
        # Keep FP32 and eval mode; no quantization or reduced image resolution.
        dino_model.to(_target_device).eval()
        _new_dino_manifest['device'] = _target_device

    try:
        _new_engine = {}
        for _name in function_names:
            _f = _new_vote if _name == 'generate_vote' else globals()[_name]
            while hasattr(_f, '__wrapped__'):
                _f = _f.__wrapped__
            _new_engine[_name] = code_signature(_f.__code__)
        _new_common['engine'] = hashlib.sha256(json.dumps(_new_engine, sort_keys=True).encode()).hexdigest()
        _new_common['dino'] = _new_dino_manifest
        _new_common['runtime_optimization'] = 'gpu-dino-cleanup-v1'
        _new_common = json.loads(json.dumps(_new_common, default=str))
        _new_manifest = dict(_new_common, preset=PRESET)
        # Explicit migration: keep the original manifest and the exact old/new boundary.
        atomic_json(_folder / f'run_config.before_speed_{_stamp}.json', _old_manifest)
        atomic_json(_folder / f'speed_transition_{_stamp}.json', {
            'utc': _stamp, 'completed_item_files': _saved_items,
            'old_manifest': _old_manifest, 'new_manifest': _new_manifest,
            'note': 'Existing results retained. Same decision logic and budgets. DINO CPU to GPU may cause numerical differences.'})
        atomic_json(_manifest_path, _new_manifest)
    except BaseException:
        if CROP_BACKEND == 'dinov3':
            dino_model.to(_old_dino_device)
        raise
    generate_vote = _new_vote
    common_manifest = _new_common
    dino_manifest = _new_dino_manifest
    if CROP_BACKEND == 'dinov3':
        DINO_DEVICE = _target_device
        _loaded_dino_key = (DINO_MODEL_ID, DINO_REVISION, DINO_DEVICE, OFFLINE)
    _dino_box_cache = None
    _gemma_speed_applied = True
    print(f'완료된 체크포인트 {len(_saved_items)}개 보존. 패치 적용 완료.')
    print(f'DINO 장치: {DINO_DEVICE}. TTA/Thinking/이미지 토큰 상한은 그대로입니다.')
    print('8번 셀만 다시 실행하세요. 1~7번 재실행 또는 런타임 재시작은 하지 마세요.')
