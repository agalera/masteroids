/*
 * masteroids_server.hpp
 *
 *  Created on: 01/02/2014
 *      Author: qaruk
 */

#ifndef MASTEROIDS_SERVER_HPP_
#define MASTEROIDS_SERVER_HPP_


#ifndef MASTEROIDS_MAIN_H_
#define MASTEROIDS_MAIN_H_

#include <stddef.h>
#include <string>
#include <iostream>

#include <json/json.h>
#include <ctime>
#include <cmath>
#include <cstdlib>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <list>
#include <netdb.h>
#include <stdexcept>

// box2d
#include <Box2D/Box2D.h>

// sockets include
#include <sys/types.h>
#include <sys/socket.h>

// Game Classes
#include "classes/client.hpp"
#include "classes/asteroids.hpp"
#include "classes/bullet.hpp"
#include "classes/destructorListener.hpp"
#include "classes/contactListener.hpp"
#include "classes/shoot.hpp"

// Game listeners
#include "classes/destructorListener.hpp"

#define MASTEROIDS_SERVER_PORT 8003
#define MASTEROIDS_SERVER_IP "127.0.0.1"


using namespace masteroids;


///////////////////////////////////////////////
//
// __main__
//
///////////////////////////////////////////////

///////////////////////////////////////////////

std::clock_t getDelta( int &last_frame );

std::clock_t getTime();

void updateFPS( int &fps, clock_t &last_time );


class MainProcess
{

  // life cicle
public:
  MainProcess();

  ~MainProcess();

  // interface
public:

  void run();

  // attributes
private:

//  std::list< Client > list_of_clients_;

//  std::list< Bullet > list_of_bullets_;
//
//  std::list< Asteroids > list_of_asteroids_;

  bool delete_bullet_;

  int delete_bullet_num_;

  bool delete_asteroid_;

  int delete_asteroid_num_;

};




#endif /* MASTEROIDS_SERVER_HPP_ */
