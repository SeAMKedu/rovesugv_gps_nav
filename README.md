![hankelogo](/images/rovesugv_logo.png)

# rovesugv_gps_nav
ROS 2 -paketti Husarion Panther -mobiilirobotin GPS-navigointia varten.

## Ohjelmistoriippuvuudet
```
$ sudo apt install ros-humble-spatio-temporal-voxel-layer
```

## Ohjelmien käynnistys

### Fixposition
Ota SSH-yhteys NVidia Jetson -tietokoneeseen ja käynnistä Fixposition-laitteen ROS 2 -ajuri alla olevilla komennoilla.
```
$ cd ros_ws/
$ source install/setup.bash
$ ros2 launch fixposition_driver_ros2 node.launch
```
Mene sitten verkkoselaimella osoitteeseen [http://10.15.20.4](http://10.15.20.4) ja käynnistä sensorifuusio sinisestä **Start**-painikkeesta. Kun fuusio on käynnistynyt, kalibroi Fixposition-laitteen sisäinen IMU-yksikkö ajamalla venytettyä numero kahdeksaa muistuttavaa rataa.

### Nav2
Alla olevat komennot ajetaan Ubuntu-kannettavalla. Komennot ajetaan omissa terminaaleissaan. 

Kiinteä koordinaatistomuunnos **vrtk_link** --> **panther/base_link**:
```
$ source install/setup.bash
$ ros2 launch rovesugv_gps_nav fixposition.launch.py
```
**FromLL**-palvelun käynnistys:
```
$ source install/setup.bash
$ ros2 launch rovesugv_gps_nav navsat.launch.py
```
**Mapviz**-ohjelman käynnistys:
```
$ source install/setup.bash
$ ros2 launch rovesugv_gps_nav mapviz.launch.py
```
**Nav2**-paketin käynnistys:
```
$ source install/setup.bash
$ ros2 launch rovesugv_gps_nav navigation.launch.py
```
ROS 2 -solmu, joka käynnistää navigoinnin Mapviz-kartalla klikattuun pisteeseen:
```
$ source install/setup.bash
$ ros2 run rovesugv_gps_nav interactive_waypoint_commander
```
**/cmd_vel** aiheen tilaus ja julkaistujen viestien lähetys **/panther/cmd_vel** aiheeseen.
```
$ source install/setup.bash
$ ros2 run rovesugv_gps_nav cmd_vel_converter
```

## RovesUGV-hanke

RovesUGV-hanke keskittyy autonomisten logistiikkaratkaisujen kehittämiseen ja demonstrointiin Roveksen teollisuusalueella. Hankkeen tarpeen taustalla on Roveksen ja Kapernaumin teollisuusalueiden yritysten välinen jatkuva logistiikka ja tavaraliikenne, joka nykyisin toimii yritysten oman työvoiman, pakettiautojen, ja isompien kuorma-autojen avulla. Hankkeen tavoitteena on kehittää Proof-of-Concept (PoC) demo, jossa tavaraa siirretään autonomisesti Husarion Panther UGV -mobiilirobotin avulla.

* Hankkeen nimi: RovesUGV
* Hankkeen aikataulu: 01.04.2025 - 31.07.2026
* Hankkeen rahoittaja: Etelä-Pohjanmaan liitto, Euroopan aluekehitysrahasto (EAKR)

---
![eakr_logo](/images/Euroopan_unionin_osarahoittama_POS.png)

![epliitto_logo](/images/EPLiitto_logo_vaaka_vari.jpg)

![seamk_logo](/images/SEAMK_vaaka_fi_en_RGB_1200x486.jpg)