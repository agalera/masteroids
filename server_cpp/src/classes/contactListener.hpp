#ifndef MASTEROIDS_CONTACT_LISTENER_H_
#define MASTEROIDS_CONTACT_LISTENER_H_

#include <iostream>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>

#include <Box2D/Box2D.h>

namespace masteroids
{


class MasteroidsContactListerner : public b2ContactListener
{

  // life cicle
public:
  MasteroidsContactListerner();

  ~MasteroidsContactListerner();

  // interface
public:

  void beginContact( const b2Contact& contact );

  void endContact( const b2Contact& contact );

  void postSolve( const b2Contact& contact, const b2ContactImpulse& impulse );

  void add( const b2Vec2& point );

  void persist( const b2Vec2& point );

  void remove( const b2Vec2& point );

  // attributes
private:

};

}

#endif
