.global	_fragment_shader_source
.global	_fragment_shader_source_size
_fragment_shader_source:
.incbin "native/fragment.glsl"
_fragment_shader_source_size:
.long _fragment_shader_source_size - _fragment_shader_source
