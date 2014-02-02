#ifndef MASTEROIDS_CLIENT_H_
#define MASTEROIDS_CLIENT_H_

#include <iostream>
#include <stdlib.h> /* among others srand, rand */
#include <cmath>

#include <list>

// Physics library
#include <Box2D/Box2D.h>

// sockets include
#include <sys/types.h>
#include <sys/socket.h>

#include "bullet.hpp"

namespace masteroids
{


class Client
{

  // life cicle
public:
  Client();

  ~Client();

  // Interface
public:

  void setWorld ( const b2World &world );

  b2World getWorld () const;

  b2World& refWord () const;

  void setBody ( const b2Body &body );

  b2Body getBody() const;

  b2Body& refBody() const;

  void setStatusAlive( const bool status_alive );

  bool isStatusAlive();

  void setChangeEnergy( const bool change_energy );

  bool isChangeEnergy() const;

  void setEnergy( const float energy );

  float getEnergy() const;

  void setChangeHealth( const bool change_health );

  bool isChangeHealth() const;

  void setHealth( const float health );

  float getHealth() const;

  // Atributes
private:

  std::list < Bullet > bullet_array_;

  b2World world_;

  b2Body body_;

  bool status_alive_;

  bool change_energy_;

  float energy_;

  bool change_health_;

  float health_;

};

}

#endif
