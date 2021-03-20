#include <SD.h>                           //include SD module library
#include <TMRpcm.h>                       //include speaker control library

#define SD_ChipSelectPin 4                

TMRpcm tmrpcm;                            //crete an object for speaker library

void setup(){
  
  tmrpcm.speakerPin = 9;                  
                                         
  if (!SD.begin(SD_ChipSelectPin)) {      //Check if the card is present and can be initialized
    
    return;                            
  }
  
  tmrpcm.setVolume(6);                    //0 to 7. Set volume level
  tmrpcm.play("1.wav");         //the sound file "1" will play each time the arduino powers up, or is reset
}

void loop(){}
