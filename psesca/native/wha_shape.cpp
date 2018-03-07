#include "wha_shape.hpp"

#include <iostream>
#include <algorithm>
#include <glm/mat4x4.hpp>
#include <glm/vec4.hpp>

WHAShape::WHAShape(float w, float h, float a) :
	width(w), height(h), area(a)
{
}

WHAShape::~WHAShape()
{
}

void WHAShape::getStrips(
		std::vector<GLfloat> &stripsComponents,
		std::vector<GLfloat> &stripsNormals,
		std::vector<unsigned short> &stripsIndexes,
		std::vector<GLsizei> &stripsCount,
		glm::mat4 &trans) const
{
	float depth = std::min(width, height);
	glm::vec4 v[8];
	int iV = 0;
	for(int x = -1; x <= 1; x += 2) {
		for(int y = -1; y <= 1; y += 2) {
			for(int z = 0; z <= 1; z += 1) {
				glm::vec4 v0(x * width/2, y * height/2, z*depth, 1.0);
				v[iV++] = trans * v0;
			}
		}
	}

	int verticesI[20] = {
		0, 1, 2, 3,
		2, 3, 6, 7,
		6, 7, 4, 5,
		4, 5, 0, 1,
		1, 3, 5, 7
	};
	float normals[] = {
		-1, 0, 0,
		0, 1, 0,
		1, 0, 0,
		0, -1, 0,
		0, 0, 1};


	int offset = stripsComponents.size() / 3;
	for(int iS = 0; iS < 5; iS ++) {
		for(iV = 4*iS; iV < 4*iS+4; iV++) {
			for(int d = 0; d < 3; d++) {
				stripsComponents.push_back(v[verticesI[iV]][d]);
				stripsNormals.push_back(normals[3*iS + d]);
			}
			stripsIndexes.push_back(offset + iV);
		}
		stripsCount.push_back(4);
	}
}
