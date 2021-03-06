#ifndef SMEAR_H
#define SMEAR_H

#include "interface/Event.hpp"
#include "interface/Named.hpp"

#define SMEAR_OK 0
#define SMEAR_NA 1
#define SMEAR_UNKOWN_FAIL 2

// -------------------- DEFINE SMEARERs --------------

class SmearBase : public Named {
    public:

        SmearBase(){};
        ~SmearBase(){};

        // ---
        string name_ = "NONE";
        int syst_{0};
        const inline string name() const {
            if (syst_ == 0 ) return name_;
            else if (syst_ >0 ) return name_ + "Up" ; // this name should be consistent with datacards
            else  return name_ + "Down" ;
        }
        //const inline string operator(){return name();};
        virtual void inline SetSyst(int s){syst_=s;}
        // ---
        virtual int smear(Event *e){return 0;}; // 0 = success; 1 not applicable to the event
        virtual inline vector<Jet*> &GetJets(Event *e){return e->jets_;}
        virtual inline vector<Tau*> &GetTaus(Event *e){return e->taus_;}
        virtual inline Met &GetMet(Event *e){return e->met_;}
};

class SmearLepSF : virtual public SmearBase
{
    public:
        SmearLepSF() :SmearBase(){ Log(__FUNCTION__,"WARNING","Obsolete. Use SmearSF");name_= "LEPSF";}
        virtual int smear(Event *e);
};

class SmearJes : virtual public SmearBase
{
    public:
        SmearJes() : SmearBase(){ name_ = "JES";}
        virtual int smear(Event*e);	
};

class SmearTauScale : virtual public SmearBase
{
    public:
        SmearTauScale() : SmearBase(){ name_ = "TAUSCALE";}
        virtual int smear(Event*e);	
};

class SmearJer:virtual public SmearBase
{
    public:
        SmearJer() : SmearBase(){ name_ = "JER";}
        virtual int smear(Event*e);	

};

class SmearUncluster : virtual public SmearBase
{
    public:
        SmearUncluster() : SmearBase(){ name_ = "UNCLUSTER";}
        virtual int smear(Event*e);	
};

class SmearSF : virtual public SmearBase
{
    string sfname_{""};
    public:
        SmearSF() :SmearBase(){ name_= "SF";}
        SmearSF(string name,string sf) :SmearBase(){ name_= name; sfname_=sf;}
        virtual int smear(Event *e);
};

class SmearPu : virtual public SmearBase
{
    public:
        SmearPu() : SmearBase(){ name_ = "PU";}
        virtual int smear(Event*e);	
};

class SmearScales : virtual public SmearBase
{
    /*
     *Never tested, nor implemented the load of the Nevents Reweighted in the MC. 
     *These info  not available at the moment
     */
    bool doRen{true};
    bool doFac{true};

    public: 
        SmearScales() : SmearBase(){ name_="Scale";}
        SmearScales(string name, bool ren, bool fac) : SmearBase(){ name_=name;doRen=ren,doFac=fac;}
        virtual int smear(Event*e);	
};

class SmearPdfs : virtual public SmearBase
{
    /*
     *Never tested, nor implemented the load of the Nevents Reweighted in the MC. 
     *These info  not available at the moment
     */
    int num_; // from 0- each round I'll do 2: pos=num*2+(syst_>0)?1:0
    int GetPos() const { return num_*2 + ((syst_>0)?1:0);}
    public: 
        SmearPdfs() : SmearBase(){ name_="Pdf";num_=0;}
        SmearPdfs(int num) : SmearBase(){num_=num; name_="Pdf";}
        const inline string name() const { return  name_ + Form("%d",GetPos());}
        virtual int smear(Event*e);	
};

class SmearBjets : virtual public SmearBase
{
    /* for simple smearing, correlated use SmearSF*/
    bool doL{false},doB{false};
    string sfname_;

    public:
        SmearBjets(){}
        SmearBjets(bool bjets, bool udsc,string sf){ doL=udsc; doB=bjets; name_= string("BTAG") + ((doB)?"B":"") + ((doL)?"L":""); sfname_=sf;}
        ~SmearBjets(){}
        virtual int smear(Event*e);	
        const string sfname(){ return sfname_ ;}

};

#endif
// Local Variables:
// mode:c++
// indent-tabs-mode:nil
// tab-width:4
// c-basic-offset:4
// End:
// vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 
