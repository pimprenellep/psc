#include "cost.h"

cost::cost()
{
    float kdir;
    float kro;
    float kvelocity;
    float kpostureFree;
    float kpostureClimb;
    float kcom;
    float kforce;

    float cost(){
        1/pow(kro,2)*()
    }

    float projectionMur(vector<float> const& a ){
        return a[1];
    }

    float distanceToGoal(vector<float> const& currentPosition, vector<float> const& finalPosition, vector<int> phi){
        float d;
        for(int i(0); i<currentPosition.size(); i++){
            d = d + phi[i]*(pow(currentPosition[i]-finalPosition,2);
        }
        return d;
    }//distance to the aimed position for thoses members : lf, rf, lh, rh. Phi equals 1 when the member has to go on one specific position, 0 otherwise.
    float distanceCenterOfMass(vector<float> const& currentPosition, vector<float> const& massOfMembers){
        float d;
        for
    }
}

cost::~cost()
{
    //dtor
}
