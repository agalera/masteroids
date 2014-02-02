#include "shoot.hpp"

namespace masteroids
{


Shoot::Shoot(const b2Vec2 &init_pos, const b2Body &body)
  : pos_ ( init_pos )
  , body_ ( body )
{

}

Shoot::~Shoot()
{
  ;
}

const std::string Shoot::getType() const
{
  return ( "Shoot");
}

b2Body& Shoot::getBody()
{
  return( body_ );
}

void Shoot::setBody( const b2Body &body )
{
  body_ = body;
}

b2Vec2 Shoot::getInitPosition()
{
  return( pos_ );
}

void Shoot::setInitPostition( const b2Vec2 init_pos )
{
  pos_ = init_pos;
}

b2Vec2 Shoot::getPosition( ) const
{
  return ( pos_ );
}

}

