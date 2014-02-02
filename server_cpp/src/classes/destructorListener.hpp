#ifndef MASTEROIDS_DESTRUCTOR_LISTENER_H_
#define MASTEROIDS_DESTRUCTOR_LISTENER_H_

#include <iostream>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>

#include <Box2D/Box2D.h>

namespace masteroids
{

class MasteroidsDestructorListerner : public b2DestructionListener
{
  // life cicle
public:
  MasteroidsDestructorListerner();

  ~MasteroidsDestructorListerner();

  void SayGoodbye(b2Joint* joint);

  void SayGoodbye(b2Fixture* fixture);
};

}

#endif
