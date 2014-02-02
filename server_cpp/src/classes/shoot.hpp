#ifndef MASTEROIDS_Shoot_H_
#define MASTEROIDS_Shoot_H_

#include <cmath>
#include <stdlib.h> /* among others srand, rand */
#include <Box2D/Box2D.h>

namespace masteroids
{


class Shoot
{
public:
  Shoot( const b2Vec2&, const b2Body& );

  ~Shoot();

  const std::string getType() const;

  b2Body& getBody();

  void setBody( const b2Body& );

  b2Vec2 getInitPosition();

  void setInitPostition( const b2Vec2 init_pos );

  b2Vec2 getPosition( ) const;

private:

  b2Vec2 pos_;

  b2Body body_;
};

}

#endif
