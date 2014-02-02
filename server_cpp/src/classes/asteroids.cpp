#include "asteroids.hpp"
#include "Box2D/Box2D.h"

namespace masteroids
{


Asteroids::Asteroids(  )
  {
	;
  }

Asteroids::Asteroids( b2World* world )
  {
	assert( world != NULL );
	  world_ = *world;
	  body_definitios_ = b2BodyDef();

	  body_.SetActive( true );
	  body_.Set
  }


//Asteroids::Asteroids( const b2World& world )
//  {
//	  world_ = world;
//	  body_definitios_ = b2BodyDef();
//
//	  body_ = b2Body( &body_definitios_, &world_);
//  }

Asteroids::~Asteroids()
  {
	  ;
  }

  const b2Body Asteroids::getBody() const
  {
	  return ( body_ );
  }

  b2Body& Asteroids::refBody()
  {
	  return ( body_ );
  }

  bool Asteroids::isAwake() const
  {
	  return ( body_.IsAwake() );
  }

  void Asteroids::touch( )
  {
	  ;
  }

  void Asteroids::setWorld( const b2World& world )
  {
	  world_ = world;
  }

  void Asteroids::setTransform( const b2Transform& transform )
  {
	  ;
  }

  const b2World Asteroids::getWorld() const
  {
	  return ( world_ );
  }

  b2World& Asteroids::refWorld()
  {
	  return ( world_ );
  }

  b2Vec2 Asteroids::getPosition() const
  {
	  return ( transform_.p );
  }

  const std::string Asteroids::getType() const
  {
	  const std::string type = "Asteroids";
	  return ( type );
  }

  void Asteroids::recive_Damage( int damage )
  {
    health_ -= damage;
    // delete asteroid, from Asteroids list.
    if ( health_ <= 0 )
      {

      }
  }

  b2Body& Asteroids::generateAsterid( const b2Transform& transform )
  {
	  return( body_ );
  }

}
