//============================================================================
// Name        : msteroids_server.cpp
// Author      : Adrian Garcia
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include "masteroids_server.hpp"

//int main() {
//	std::cout << "!!!Hello World!!!" << std::endl; // prints !!!Hello World!!!
//	return 0;
//}

std::clock_t getDelta( int &last_frame )
{
  std::clock_t time = getTime();
  int delta = static_cast<float>(time - last_frame);
  last_frame = time;
  return ( delta );
}



std::clock_t getTime()
{
  return ( clock() * 1000 );
}

void updateframes_per_second( int &frames_per_second, std::clock_t &last_time )
{
  int current_frames_per_second = 0;
  std::clock_t delta_time = clock() - last_time;
  frames_per_second++;
  if( delta_time >= 1)
    {
      current_frames_per_second = (float)frames_per_second / delta_time ;
      std::cout << current_frames_per_second << " frames_per_second " << std::endl;
      frames_per_second = 0;
      last_time = clock();
    }
}


void MainProcess::run()
{

}


///////////////////////////////////////////////
//
// __main__
//
///////////////////////////////////////////////

int main( void )
{
	std::cout << "¡¡¡Start Masteroids server!!!" << std::endl; // prints !!!UDP server!!!

	/*
	 * Variables
	 */
	std::clock_t last_time = clock();
	std::clock_t last_frame = clock();

	float t_delta = 0;
	float animate = 0.0;

	int frames_per_second = 0;
	int last_frames_per_second = 0;

	float time_step = 1.0 / 160.0;

	int velocity_iterator = 6;
	int position_iterator = 2;

	int number_of_inital_asteroids = 200;

	/*
	 * Configure UPD server
	 */

	int server_port = MASTEROIDS_SERVER_PORT;
	const std::string server_addres = MASTEROIDS_SERVER_IP;

	udp_server masteroids_server = udp_server(server_addres, server_port);

	/*
	 * Configure lists: clients, asteroids
	 */

  // List of Clients
  std::list< Client > client_list();

  // list with numberOfInitialAsteroids default build
  std::list< Asteroids > asteroid_list();

  // world conditions
  b2Vec2 gravity = b2Vec2( 0.0, 0.0 );
  b2ContactFilter* contacListener = new b2ContactFilter();
  MasteroidsDestructorListerner* destructorListener = new MasteroidsDestructorListerner();

  b2World world = b2World( gravity );
  world.SetContactFilter( contacListener );
  world.SetDestructionListener( destructorListener );

  for ( int asteroid_it = 0; asteroid_it << number_of_inital_asteroids ; asteroid_it++ )
    {
      Asteroids new_asteroid = Asteroids( );
      asteroid_list().push_back( new_asteroid );
    }




  return ( 0 );
}


