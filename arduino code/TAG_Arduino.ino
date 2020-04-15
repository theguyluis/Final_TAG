/**
 * --------------------------------------------------------------------------------------------------------------------
 * Example sketch/program showing how to read data from more than one PICC to serial.
 * --------------------------------------------------------------------------------------------------------------------
 * This is a MFRC522 library example; for further details and other examples see: https://github.com/miguelbalboa/rfid
 *
 * Example sketch/program showing how to read data from more than one PICC (that is: a RFID Tag or Card) using a
 * MFRC522 based RFID Reader on the Arduino SPI interface.
 *
 * Warning: This may not work! Multiple devices at one SPI are difficult and cause many trouble!! Engineering skill
 *          and knowledge are required!
 *
 * @license Released into the public domain.
 *
 * Typical pin layout used:
 * -----------------------------------------------------------------------------------------
 *             MFRC522      Arduino       Arduino   Arduino    Arduino          Arduino
 *             Reader/PCD   Uno/101       Mega      Nano v3    Leonardo/Micro   Pro Micro
 * Signal      Pin          Pin           Pin       Pin        Pin              Pin
 * -----------------------------------------------------------------------------------------
 * RST/Reset   RST          9             5         D9         RESET/ICSP-5     RST
 * SPI SS 1    SDA(SS)      ** custom, take a unused pin, only HIGH/LOW required **
 * SPI SS 2    SDA(SS)      ** custom, take a unused pin, only HIGH/LOW required **
 * SPI MOSI    MOSI         11 / ICSP-4   51        D11        ICSP-4           16
 * SPI MISO    MISO         12 / ICSP-1   50        D12        ICSP-1           14
 * SPI SCK     SCK          13 / ICSP-3   52        D13        ICSP-3           15
 
 */
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9          // Configurable, see typical pin layout above
#define SS_1_PIN        3         // Configurable, take a unused pin, only HIGH/LOW required, must be diffrent to SS 2
#define SS_2_PIN        6          // Configurable, take a unused pin, only HIGH/LOW required, must be diffrent to SS 1
#define SS_3_PIN        8

#define NR_OF_READERS   3
// Comparing the strings of the UID vars
String Reader_0_tmp="";
String Reader_1_tmp="";
String Reader_2_tmp="";

MFRC522 mfrc522_Reader0(SS_1_PIN,RST_PIN); // Create a MFRC522 instance for reader 0
MFRC522 mfrc522_Reader1(SS_2_PIN,RST_PIN); // Create a MFRC522 instance for reader 1
MFRC522 mfrc522_Reader2(SS_3_PIN,RST_PIN); // Create a MFRC522 instance for reader 2
void setup() 
{
  Serial.begin(9600); // Initialize serial communications with the PC
  while (!Serial);    // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)

  SPI.begin();        // Init SPI bus
  mfrc522_Reader0.PCD_Init();
  mfrc522_Reader1.PCD_Init();
  mfrc522_Reader2.PCD_Init();
  //Serial.println("Put your card to the reader...");
}

void loop() 
{
  Card_Reader_0();
  Card_Reader_1();
  Card_Reader_2();
}

void Card_Reader_0()
{
  // Want to look for a new card int reader 0
  if(!mfrc522_Reader0.PICC_IsNewCardPresent())
  {
    //return;
  }
  if(!mfrc522_Reader0.PICC_ReadCardSerial())
  {
    //return;
  }
  String Reader0_content="";
  for(byte i=0; i<mfrc522_Reader0.uid.size;i++)
  {
    Reader0_content.concat(String(mfrc522_Reader0.uid.uidByte[i] < 0x10? " 0":" "));
    Reader0_content.concat(String(mfrc522_Reader0.uid.uidByte[i], HEX));
    Reader0_content.toUpperCase();
  }
  //Serial.println();
  
  if(Reader0_content.substring(1) == Reader_0_tmp)
  {
    // Just need it to do nothing could make this the else statment....
    //return;
    // Debug testing code for duplicates
    //Serial.print("Card has been previously scanned");
  }
  else
  {
    Reader_0_tmp = Reader0_content.substring(1);
    Serial.print("Reader_0:");
    Serial.println(Reader0_content.substring(1));
    //Serial.println();
  }
  mfrc522_Reader0.PICC_HaltA();
  mfrc522_Reader0.PCD_StopCrypto1();
}



void Card_Reader_1()
{
  // Want to look for a new card int reader 0
  if(!mfrc522_Reader1.PICC_IsNewCardPresent())
  {
    //return;
  }
  if(!mfrc522_Reader1.PICC_ReadCardSerial())
  {
    //return;
  }
  String Reader1_content="";
  for(byte i=0; i<mfrc522_Reader1.uid.size;i++)
  {
    Reader1_content.concat(String(mfrc522_Reader1.uid.uidByte[i] < 0x10? " 0":" "));
    Reader1_content.concat(String(mfrc522_Reader1.uid.uidByte[i], HEX));
    Reader1_content.toUpperCase();
  }
  //Serial.println();
  
  if(Reader1_content.substring(1) == Reader_1_tmp)
  {
    // Just need it to do nothing could make this the else statment....
    //return;
    // Debug testing code for duplicates
    //Serial.print("Card has been previously scanned");
  }
  else
  {
    Reader_1_tmp = Reader1_content.substring(1);
    Serial.print("Reader_1:");
    Serial.println(Reader1_content.substring(1));
  }
  mfrc522_Reader1.PICC_HaltA();
  mfrc522_Reader1.PCD_StopCrypto1();
}




void Card_Reader_2()
{
  // Want to look for a new card int reader 0
  if(!mfrc522_Reader2.PICC_IsNewCardPresent())
  {
    //return;
  }
  if(!mfrc522_Reader2.PICC_ReadCardSerial())
  {
    //return;
  }
  String Reader2_content="";
  for(byte i=0; i<mfrc522_Reader2.uid.size;i++)
  {
    Reader2_content.concat(String(mfrc522_Reader2.uid.uidByte[i] < 0x10? " 0":" "));
    Reader2_content.concat(String(mfrc522_Reader2.uid.uidByte[i], HEX));
    Reader2_content.toUpperCase();
  }
  //Serial.println();
  
  if(Reader2_content.substring(1) == Reader_2_tmp)
  {
    // Just need it to do nothing could make this the else statment....
    //return;
    // Debug testing code for duplicates
    //Serial.print("Card has been previously scanned");
  }
  else
  {
    Reader_2_tmp = Reader2_content.substring(1);
    Serial.print("Reader_2:");
    Serial.println(Reader2_content.substring(1));
  }
  mfrc522_Reader2.PICC_HaltA();
  mfrc522_Reader2.PCD_StopCrypto1();
}
