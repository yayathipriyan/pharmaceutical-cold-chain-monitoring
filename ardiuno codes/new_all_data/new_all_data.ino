#include <TinyGPS++.h> // library for GPS module
#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include<DHT.h>
TinyGPSPlus gps;
DHT dht2(2,DHT11); 
SoftwareSerial ss(4, 5);
float temp,humi,vibr;
//SoftwareSerial ss(12,14);// The serial connection to the GPS device
const char* ssid = "motorola one fusion+"; //ssid of your wifi
const char* password = "golem@llr9"; //password of your wifi
float latitude , longitude;
int year , month , date, hour , minute , second;
String date_str , time_str , lat_str , lng_str;
long val;
int pm;
#define vib D0  
WiFiServer server(80);

void setup()
{
  Serial.begin(115200);
  ss.begin(9600);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password); //connecting to wifi
  while (WiFi.status() != WL_CONNECTED)// while wifi not connected
  {
    delay(500);
    Serial.print("."); //print "...."
  }
  Serial.println("");
  Serial.println("WiFi connected");
  server.begin();
  Serial.println("Server started");
  Serial.println(WiFi.localIP());  // Print the IP address
}


void loop()
{
  while (ss.available() > 0) //while data is available
    {
         if (gps.encode(ss.read())) //read gps data
    {
      if (gps.location.isValid()) //check whether gps location is valid
      {
        latitude = gps.location.lat();
        lat_str = String(latitude , 6); // latitude location is stored in a string
        longitude = gps.location.lng();
        lng_str = String(longitude , 6); //longitude location is stored in a string
      }
      if (gps.date.isValid()) //check whether gps date is valid
      {
        date_str = "";
        date = gps.date.day();
        month = gps.date.month();
        year = gps.date.year();
        if (date < 10)
          date_str = '0';
        date_str += String(date);// values of date,month and year are stored in a string
        date_str += " / ";

        if (month < 10)
          date_str += '0';
        date_str += String(month); // values of date,month and year are stored in a string
        date_str += " / ";
        if (year < 10)
          date_str += '0';
        date_str += String(year); // values of date,month and year are stored in a string
      }
      if (gps.time.isValid())  //check whether gps time is valid
      {
        time_str = "";
        hour = gps.time.hour();
        minute = gps.time.minute();
        second = gps.time.second();
        minute = (minute + 30); // converting to IST
        if (minute > 59)
        {
          minute = minute - 60;
          hour = hour + 1;
        }
        hour = (hour + 5) ;
        if (hour > 23)
          hour = hour - 24;   // converting to IST
        if (hour >= 12)  // checking whether AM or PM
          pm = 1;
        else
          pm = 0;
        hour = hour % 12;
        if (hour < 10)
          time_str = '0';
        time_str += String(hour); //values of hour,minute and time are stored in a string
        time_str += " : ";
        if (minute < 10)
          time_str += '0';
        time_str += String(minute); //values of hour,minute and time are stored in a string
        time_str += " : ";
        if (second < 10)
          time_str += '0';
        time_str += String(second); //values of hour,minute and time are stored in a string
        if (pm == 1)
          time_str += " PM ";
        else
          time_str += " AM ";
      }  
    }
        
        Serial.println("*************");
        hour = gps.time.hour();
        minute = gps.time.minute();
        second = gps.time.second();

        latitude = gps.location.lat();
        lat_str = String(latitude , 6); // latitude location is stored in a string
        longitude = gps.location.lng();
        lng_str = String(longitude , 6);
          
        temp=dht2.readTemperature();
        humi=dht2.readHumidity();
        Serial.print("Temperature in C:");  
        Serial.println();  
        Serial.print("Humidity in C:"); 
        Serial.println(dht2.readHumidity());

        Serial.print("Lattitude : ");
        Serial.println(lat_str);
        Serial.print("Longitude : ");
        Serial.println(lng_str);
        Serial.print("Time : ");
        Serial.println(time_str);
        Serial.print("Date : ");
        Serial.println(date_str);
        val = digitalRead(vib);
        Serial.print("vibration : ");
        Serial.println(val);
        
        Serial.println("*************");
        
    }
    
    delay(5000);
 WiFiClient client = server.available(); // Check if a client has connected
  if (!client)
  {
    return;
  }
  // Prepare the response
  String s = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n <!DOCTYPE html> <html>";
  s+="<h1> All Sensor data</h1>";
  s+="<pre>";
  s+="<h4>Temperature : ";
  s+=temp;
  s+="</h4>";
  s+="<h4>Humidity : ";
  s+=humi;
  s+="</h4>";
  s+="<h4>Vibration : ";
  s+=val;
  s+="</h4>";
  s+="<h4> Lattitude : ";
  s+=lat_str;
  s+="</h4>";
  s+="<h4> Longitude : ";
  s+=lng_str;
  s+="</h4>";
  s+="<h4> Date : ";
  s+=date_str;
  s+="</h4>";
  s+="<h4> Time : ";
  s+=time_str;
  s+="</h4>";
  s+="</pre>";
  s += "</body> </html>";

  client.print(s); // all the values are send to the webpage
  delay(100);
}
