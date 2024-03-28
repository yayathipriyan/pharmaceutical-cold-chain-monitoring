#include <ESP8266WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include<DHT.h>
DHT dht2(2,DHT11);
WiFiServer server(80);
// Replace with your network credentials
const char *ssid     = "motorola one fusion+";
const char *password = "yayathi@alienx";

// Define NTP Client to get time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

//Week Days
String weekDays[7]={"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

//Month names
String months[12]={"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};

void setup() {
  // Initialize Serial Monitor
  Serial.begin(9600);
  
  // Connect to Wi-Fi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  server.begin();
// Initialize a NTPClient to get time
  timeClient.begin();
  // Set offset time in seconds to adjust for your timezone, for example:
  // GMT +1 = 3600
  // GMT +8 = 28800
  // GMT -1 = -3600
  // GMT 0 = 0
  timeClient.setTimeOffset(19800);
}

void loop() {
  timeClient.update();
  time_t epochTime = timeClient.getEpochTime();
  String formattedTime = timeClient.getFormattedTime();
  Serial.print("Formatted Time : ");
  Serial.print(formattedTime);  
  int currentHour = timeClient.getHours();
  int currentMinute = timeClient.getMinutes();
  int currentSecond = timeClient.getSeconds();
  String weekDay = weekDays[timeClient.getDay()];
  struct tm *ptm = gmtime ((time_t *)&epochTime); 
  int monthDay = ptm->tm_mday;
  int currentMonth = ptm->tm_mon+1;
  String currentMonthName = months[currentMonth-1];
  int currentYear = ptm->tm_year+1900;
  String currentDate = String(currentYear) + "-" + String(currentMonth) + "-" + String(monthDay);
  Serial.println();
  Serial.print("Current date : ");
  Serial.print(currentDate);
  Serial.println("");
  int temp=dht2.readTemperature();
  int humi=dht2.readHumidity();
  Serial.println("Temperature :");
  Serial.print(temp);
  Serial.println("");
  Serial.println("Humidity : ");
  Serial.print(humi);
  delay(2000);
  WiFiClient client = server.available(); // Check if a client has connected
  if (!client)
  {
    return;
  }
  String s = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n <!DOCTYPE html> <html>";
  s+="<h1> All Sensor data</h1>";
  s+="<pre>";
  s+="<p id=temp>Temperature : ";
  s+=temp;
  s+="</p>";
  s+="<p id=humi>Humidity : ";
  s+=humi;
  s+="</p>";
  s+="<p id=date> Date : ";
  s+=currentDate;
  s+="</p>";
  s+="<p id=time> Time : ";
  s+=formattedTime;
  s+="</p>";
  s+="</pre>";
  s += "</body> </html>";
  delay(2000);
  client.print(s); 

}