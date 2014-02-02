#include "contactListener.hpp"

namespace masteroids
{


// life cicle
MasteroidsContactListerner::MasteroidsContactListerner()
  : b2ContactListener()
{

}

MasteroidsContactListerner::~MasteroidsContactListerner()
{
  ;
}

// interface
void MasteroidsContactListerner::beginContact( const b2Contact& contact )
{
  ;
}

void MasteroidsContactListerner::endContact( const b2Contact& contact )
{
  ;
}

void MasteroidsContactListerner::postSolve( const b2Contact& contact, const b2ContactImpulse& impulse )
{

}

void MasteroidsContactListerner::add( const b2Vec2& point )
{
  std::cout << "Add: " << point.x << " " << point.y << std::endl;
}

void MasteroidsContactListerner::persist( const b2Vec2& point )
{
  std::cout << "Persist: " << point.x << " " << point.y << std::endl;
}

void MasteroidsContactListerner::remove( const b2Vec2& point )
{
  std::cout << "Remove: " << point.x << " " << point.y << std::endl;
}

}
