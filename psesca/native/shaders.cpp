#include "shaders.hpp"

extern const char _vertex_shader_source;
extern const unsigned long _vertex_shader_source_size;

extern const char _fragment_shader_source;
extern const unsigned long _fragment_shader_source_size;

const char * Shaders::getVertexSource()
{
	return &_vertex_shader_source;
}

const unsigned long Shaders::getVertexSize()
{
	return _vertex_shader_source_size;
}

const char * Shaders::getFragmentSource()
{
	return &_fragment_shader_source;
}

const unsigned long Shaders::getFragmentSize()
{
	return _fragment_shader_source_size;
}
