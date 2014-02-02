#include "client.hpp"



Client::Client()
{

}

Client::~Client()
{
  ;
}

// Interface

void Client::setWorld ( const b2World &world )
{
  world_ = world;
}

b2World Client::getWorld () const
{
  return ( world_ );
}

b2World& Client::refWord () const
{
  return ( *world_ );
}

void Client::setBody ( const b2Body &body )
{
  body_ = body;
}

b2Body Client::getBody() const
{
  return ( body_ );
}

b2Body& Client::refBody() const
{
  return ( *body_ );
}

void Client::setStatusAlive( const bool status_alive )
{
 status_alive_ = status_alive;
}

bool Client::isStatusAlive()
{
  return (status_alive_);
}

void Client::setChangeEnergy( const bool change_energy )
{
  change_energy_ = change_energy;
}

bool Client::isChangeEnergy() const
{
  return ( change_energy_ );
}

void Client::setEnergy( const float energy )
{
  energy_ = energy;
}

float Client::getEnergy() const
{
  return ( energy_ );
}

void Client::setChangeHealth( const bool change_health )
{
  change_energy_ = change_health;
}

bool Client::isChangeHealth() const
{
  return ( change_health_ );
}

void Client::setHealth( const float health )
{
  health_ = health;
}

float Client::getHealth() const
{
  return ( health_ );
}
