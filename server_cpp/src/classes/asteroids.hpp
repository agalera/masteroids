#ifndef MASTEROIDS_ASTEROIDS_H_
#define MASTEROIDS_ASTEROIDS_H_

#include <cmath>
#include <Box2D/Box2D.h>
#include <string>
//#include "../structures/position.h"
#include <stdlib.h> /* among others srand, rand */

namespace masteroids
{


class Asteroids
{

public:

	Asteroids( );

	Asteroids( b2World* world )

  Asteroids( const b2World& world );

  ~Asteroids();

  const b2Body getBody() const;

  b2Body& refBody();

  bool isAwake() const;

  void touch( );

  void setWorld( const b2World& world );

  void setTransform( const b2Transform& transform );

  const b2World getWorld() const;

  b2World& refWorld();

  b2Vec2 getPosition() const;

  const std::string getType() const;

  void recive_Damage( int damage );

private:

  b2Body& generateAsterid( const b2Transform& transform );

private:

  b2BodyDef body_definitios_;

  b2Body body_;

  b2World world_;

  b2Transform transform_;

  int health_;


};

}

#endif
