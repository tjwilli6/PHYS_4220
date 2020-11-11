#include <cmath>
#include <iostream>
#include <fstream>
using namespace std;
int main(int argc, char *argv[])
{
  double theta0 = std::stod(argv[1]);
  double Q      = std::stod(argv[2]);
  double wd     = std::stod(argv[3]);
  double A      = std::stod(argv[4]);
  int niter     = std::stoi(argv[5]);
  double dt     = std::stod(argv[6]);
  double deriv;
  double tstop = 2 * M_PI * niter;
    const int SIZE = tstop / dt + 1;
  double omegaPrev,thetaPrev;
  double omegaCur, thetaCur;
  omegaPrev = 0;
  thetaPrev = M_PI / 180 * theta0;

  ofstream myfile( "pend_data.dat" );
  myfile << "T\tOMEGA\tTHETA\n";
  myfile << 0 << "\t" << omegaPrev << "\t" << thetaPrev << "\n";
  for( int i=1; i<SIZE; ++i)
  {
    deriv = -sin( thetaPrev ) - Q * omegaPrev + A * sin( wd * ( i*dt) );
    omegaCur = omegaPrev + deriv * dt;
    thetaCur = thetaPrev + omegaCur * dt;

    if ( thetaCur > M_PI )
      {
	thetaCur -= 2 * M_PI;
      }
    else if ( thetaCur < -M_PI )
      {
	thetaCur += 2 * M_PI;
      }
    omegaPrev = omegaCur;
    thetaPrev = thetaCur;
    myfile << i*dt << "\t" << omegaPrev << "\t" << thetaPrev << "\n";
  }
  myfile.close();
  return 0;
}
