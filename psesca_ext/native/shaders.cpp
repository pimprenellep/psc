#include "shaders.hpp"

#include "shaders_data.hpp"

const char vertex_shader_source[] = { VERTEX_SHADER_SOURCE };

const char fragment_shader_source[] = { FRAGMENT_SHADER_SOURCE };

const char * Shaders::getVertexSource()
{
	return vertex_shader_source;
}

const unsigned long Shaders::getVertexSize()
{
	return sizeof(vertex_shader_source);
}

const char * Shaders::getFragmentSource()
{
	return fragment_shader_source;
}

const unsigned long Shaders::getFragmentSize()
{
	return sizeof(fragment_shader_source);
}
