#ifndef MASTEROIDS_BULLET_H_
#define MASTEROIDS_BULLET_H_


#include <iostream>
#include <stdlib.h> /* among others srand, rand */
#include <cmath>

// Physics library
#include <Box2D/Box2D.h>

namespace masteroids
{


class Bullet
{
  // life cicle
public:
	Bullet( );

  ~Bullet();

  // Interface
public:


  // Atributtes
private:

  b2World world;


  b2Body body_;

};

}

#endif
