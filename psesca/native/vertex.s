.global	_vertex_shader_source
.global	_vertex_shader_source_size
_vertex_shader_source:
.incbin "native/vertex.glsl"
_vertex_shader_source_size:
.long _vertex_shader_source_size - _vertex_shader_source
