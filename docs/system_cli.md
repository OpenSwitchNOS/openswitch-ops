# System commands


## Contents

- [System configuration commands](#system-configuration-commands)
  - [Setting the fan speed](#setting-the-fan-speed)
  - [Unsetting the fan speed](#unsetting-the-fan-speed)
  - [Setting an LED state](#setting-an-led-state)
  - [Unsetting an LED state](#unsetting-an-led-state)
  - [Setting Timezone on the switch](#setting-timezone-on-the-switch)
  - [Unsetting Timezone on the switch](#unsetting-timezone-on-the-switch)
- [System Display Commands](#system-display-commands)
  - [Showing version information](#showing-version-information)
  - [Showing package information](#showing-package-information)
  - [Showing system information](#showing-system-information)
  - [System fan information](#system-fan-information)
  - [Showing system temperature information](#showing-system-temperature-information)
  - [Showing system LED information](#showing-system-led-information)
  - [Showing system power-supply information](#showing-system-power-supply-information)
  - [Showing system clock information](#showing-system-clock-information)
  - [Showing system cpu information using top](#showing-system-cpu-information-using-top)
  - [Showing system memory information using top](#showing-system-memory-information-using-top)
  - [Showing Timezone information](#showing-timezone-information)


## System configuration commands
### Setting the fan speed
#### Syntax
`fan-speed < normal | slow | medium | fast | maximum >`

#### Description
This command globally sets the fan speed to the value indicated by the command parameter. This command overrides the fan speed set internally by the platform. The fan speed value set by the user takes affect depending on platform cooling requirements.

#### Authority
All users.

#### Parameters
This command takes one of the following values:
- slow
- normal
- medium
- fast

By default fans operate at normal speed.

| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------------|
| *slow* | choose one| Literal | Slow is 25% of maximum speed. |
| *normal* | choose one| Literal | Normal is 40% of maximum speed. |
| *medium* | choose one| Literal | Medium is 65% of maximum speed. |
| *fast* | choose one| Literal | Fast is 80% of maximum speed. |
| *max* | choose one| Literal | Fan speed is at maximum speed. |

#### Examples

```
switch(config)#fan-speed slow
```

### Unsetting the fan speed
#### Syntax
`no fan-speed [< normal | slow | medium | fast | maximum >]`

#### Description
This command removes the configured fan speed, and sets it to the default speed.

#### Authority
All users.

#### Parameters

| Parameter | Status   | Syntax         | Description                           |
|-----------|----------|----------------------|
| *slow* | optional(choose one)| Literal | Slow is 25% of maximum speed. |
| *normal* |optional(choose one)| Literal | Normal is 40% of maximum speed. |
| *medium* | optional(choose one)| Literal | Medium is 65% of maximum speed. |
| *fast* | optional(choose one)| Literal | Fast is 80% of maximum speed. |
| *max* | optional(choose one)| Literal | Fan speed is at maximum speed. |

#### Examples
```
switch(config)#no fan-speed
```

### Setting an LED state
#### Syntax
`led < led-name > < on | flashing | off >`

#### Description
This command sets the LED state to **on**, **off**, or **flashing**. By default, the LED state is off.

#### Authority
All users.

#### Parameters
| Parameter 1| Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *led-name* | Required | Literal |LED name of whose state is to be set |


| Parameter 2| Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *off* | choose one| Literal |Select this to switch off LED |
| *on* | choose one| Literal  | Select this to switch on LED |
| *flashing*| choose one|Literal | Select this to blink/flash the LED|

#### Examples
```
switch(config)#led base-loc on
```

### Unsetting an LED state
#### Syntax
`no led <led-name> [< on | flashing | off >]`

#### Description
This command turns off the LED.

#### Authority
All users.

#### Parameters
| Parameter 1| Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *led-name* | Required | Literal | The LED name whose state is to be set. |


| Parameter 2| Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *off* | Optional(choose one)| Literal | Select this to switch the LED off. |
| *on* | Optional (choose one)| Literal  | Select this to switch the LED on. |
| *flashing*| Optional (choose one)|Literal | Select this to blink/flash the LED. |


#### Examples
```
switch(config)#no led base-loc
```

## System display commands
### Showing version information
#### Syntax
`show version`

#### Description
This command shows the current switch version information. The format of the `show version` output:
```
<name> <version> (Build: <platform>-ops-<X.Y.Z-string>-<branch-name>[-<build-time>][-<meta-string>]
```

| Field Name  | Explanation                                                                                                                          | Example                       |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| name        | Name of the project.                                                                                                                 | OpenSwitch                    |
| version     | Version of the software.                                                                                                             | 0.4.0 or 0.3.0-rc0 etc.       |
| platform    | Platform for which the image is built.                                                                                               | genericx86-64, AS5712, AS6712 |
| ops         | Abbreviation for OpenSwitch.                                                                                                         |                               |
| X.Y.Z-string| The release version tag.                                                                                                             | 0.4.0 or 0.3.0-rc0 etc.       |
| branch-name | Branch where the image is built.                                                                                                     | master, feature, release      |
| build-time  | For periodic builds, the build time-stamp in YYYYMMDDNN format. For developer builds, the build time-stamp in YYYYMMDDHHmmss format. | 2016042606, 20160419204046    |
| meta-string | “dev” is appended to image names when a developer builds an image using “make”.                                                      |                               |

#### Authority
All users.

#### Parameters
No parameters.

#### Examples
```
| Switch Image Build Type                                                 | Show version                                                                |
|-------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| Developer build of OpenSwitch from the master branch for genericx86-64. | OpenSwitch 0.4.0 (Build: genericx86-64-ops-0.4.0-master-20160419204046-dev) |
| Periodic build of OpenSwitch from the master branch for genericx86-64.  | OpenSwitch 0.4.0 (Build: genericx86-64-ops-0.4.0-master+2016042606          |
| Developer build of OpenSwitch from the master branch for AS5712.        | OpenSwitch 0.4.0 (Build: as5712-ops-0.4.0-master-20160419204046-dev)        |
| Periodic build of OpenSwitch from the master branch for AS5712.         | OpenSwitch 0.4.0 (Build: as5712-ops-0.4.0-master+2016042606)                |
| Periodic build of OpenSwitch from the release branch for AS5712.        | OpenSwitch 0.3.0-rc0 (Build: as5712-ops-0.3.0-rc0-release+2016042606)                |
```


### Showing package information
#### Syntax
`show version detail [ops]`

#### Description
This command lists every package present in the switch image under the PACKAGE column. The VERSION column displays the git hash value if the SOURCE URL is a git repository. If not, the VERSION column displays the version string of the package. SOURCE TYPE displays the type of source pointed to by SOURCE URL. SOURCE URL displays the download location for the source-code of the corresponding package in the SOURCE URI column. If version information and/or Source URL is not available during build-time, `show version detail` displays 'NA' (Not Available).

#### Authority
All users.

#### Parameters
No parameters.

| Parameter  | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
|  *ops*   | Optional | Literal | Displays git-hashes for OpenSwitch repos (ops-*) alone. |

#### Examples
```
switch#show version detail
PACKAGE     : kernel-module-gspca-spca1528
VERSION     : 3.14.36+gitAUTOINC+a996d95104_dbe5b52e93
SOURCE TYPE : git
SOURCE URL  : https://git.yoctoproject.org/linux-yocto-3.14.git;bareclone=1;branch=standard/common-pc-64/base,meta;name=machine,meta

PACKAGE     : python-jsonpatch
VERSION     : 1.11
SOURCE TYPE : http
SOURCE URL  : http://pypi.python.org/packages/source/j/jsonpatch/jsonpatch-1.11.tar.gz

PACKAGE     : ops-cli
VERSION     : a70df32190755dabf3fb404c3cde04a03aa6be40~DIRTY
SOURCE TYPE : other
SOURCE URL  : NA

PACKAGE     : dbus-1
VERSION     : NA
SOURCE TYPE : other
SOURCE URL  : NA
```
### Setting Timezone on the switch
#### Syntax
`timezone set *TIMEZONE*`

#### Description
This command sets the Timezone on the switch. By default the timezone is set to UTC (Coordinated Universal Time).

#### Authority
All users.

#### Parameters
The *TIMEZONE* parameter takes one of the following values as per the posix timezone database:
 | Parameter                     |   Description               |
 |-------------------------------|-----------------------------|
  africa/abidjan                    Africa/Abidjan Zone
  africa/accra                      Africa/Accra Zone
  africa/addis_ababa                Africa/Addis_Ababa Zone
  africa/algiers                    Africa/Algiers Zone
  africa/asmara                     Africa/Asmara Zone
  africa/asmera                     Africa/Asmera Zone
  africa/bamako                     Africa/Bamako Zone
  africa/bangui                     Africa/Bangui Zone
  africa/banjul                     Africa/Banjul Zone
  africa/bissau                     Africa/Bissau Zone
  africa/blantyre                   Africa/Blantyre Zone
  africa/brazzaville                Africa/Brazzaville Zone
  africa/bujumbura                  Africa/Bujumbura Zone
  africa/cairo                      Africa/Cairo Zone
  africa/casablanca                 Africa/Casablanca Zone
  africa/ceuta                      Africa/Ceuta Zone
  africa/conakry                    Africa/Conakry Zone
  africa/dakar                      Africa/Dakar Zone
  africa/dar_es_salaam              Africa/Dar_es_Salaam Zone
  africa/djibouti                   Africa/Djibouti Zone
  africa/douala                     Africa/Douala Zone
  africa/el_aaiun                   Africa/El_Aaiun Zone
  africa/freetown                   Africa/Freetown Zone
  africa/gaborone                   Africa/Gaborone Zone
  africa/harare                     Africa/Harare Zone
  africa/johannesburg               Africa/Johannesburg Zone
  africa/juba                       Africa/Juba Zone
  africa/kampala                    Africa/Kampala Zone
  africa/khartoum                   Africa/Khartoum Zone
  africa/kigali                     Africa/Kigali Zone
  africa/kinshasa                   Africa/Kinshasa Zone
  africa/lagos                      Africa/Lagos Zone
  africa/libreville                 Africa/Libreville Zone
  africa/lome                       Africa/Lome Zone
  africa/luanda                     Africa/Luanda Zone
  africa/lubumbashi                 Africa/Lubumbashi Zone
  africa/lusaka                     Africa/Lusaka Zone
  africa/malabo                     Africa/Malabo Zone
  africa/maputo                     Africa/Maputo Zone
  africa/maseru                     Africa/Maseru Zone
  africa/mbabane                    Africa/Mbabane Zone
  africa/mogadishu                  Africa/Mogadishu Zone
  africa/monrovia                   Africa/Monrovia Zone
  africa/nairobi                    Africa/Nairobi Zone
  africa/ndjamena                   Africa/Ndjamena Zone
  africa/niamey                     Africa/Niamey Zone
  africa/nouakchott                 Africa/Nouakchott Zone
  africa/ouagadougou                Africa/Ouagadougou Zone
  africa/porto-novo                 Africa/Porto-Novo Zone
  africa/sao_tome                   Africa/Sao_Tome Zone
  africa/timbuktu                   Africa/Timbuktu Zone
  africa/tripoli                    Africa/Tripoli Zone
  africa/tunis                      Africa/Tunis Zone
  africa/windhoek                   Africa/Windhoek Zone
  america/adak                      America/Adak Zone
  america/anchorage                 America/Anchorage Zone
  america/anguilla                  America/Anguilla Zone
  america/antigua                   America/Antigua Zone
  america/araguaina                 America/Araguaina Zone
  america/argentina/buenos_aires    America/Argentina/Buenos_Aires Zone
  america/argentina/catamarca       America/Argentina/Catamarca Zone
  america/argentina/comodrivadavia  America/Argentina/ComodRivadavia Zone
  america/argentina/cordoba         America/Argentina/Cordoba Zone
  america/argentina/jujuy           America/Argentina/Jujuy Zone
  america/argentina/la_rioja        America/Argentina/La_Rioja Zone
  america/argentina/mendoza         America/Argentina/Mendoza Zone
  america/argentina/rio_gallegos    America/Argentina/Rio_Gallegos Zone
  america/argentina/salta           America/Argentina/Salta Zone
  america/argentina/san_juan        America/Argentina/San_Juan Zone
  america/argentina/san_luis        America/Argentina/San_Luis Zone
  america/argentina/tucuman         America/Argentina/Tucuman Zone
  america/argentina/ushuaia         America/Argentina/Ushuaia Zone
  america/aruba                     America/Aruba Zone
  america/asuncion                  America/Asuncion Zone
  america/atikokan                  America/Atikokan Zone
  america/atka                      America/Atka Zone
  america/bahia                     America/Bahia Zone
  america/bahia_banderas            America/Bahia_Banderas Zone
  america/barbados                  America/Barbados Zone
  america/belem                     America/Belem Zone
  america/belize                    America/Belize Zone
  america/blanc-sablon              America/Blanc-Sablon Zone
  america/boa_vista                 America/Boa_Vista Zone
  america/bogota                    America/Bogota Zone
  america/boise                     America/Boise Zone
  america/buenos_aires              America/Buenos_Aires Zone
  america/cambridge_bay             America/Cambridge_Bay Zone
  america/campo_grande              America/Campo_Grande Zone
  america/cancun                    America/Cancun Zone
  america/caracas                   America/Caracas Zone
  america/catamarca                 America/Catamarca Zone
  america/cayenne                   America/Cayenne Zone
  america/cayman                    America/Cayman Zone
  america/chicago                   America/Chicago Zone
  america/chihuahua                 America/Chihuahua Zone
  america/coral_harbour             America/Coral_Harbour Zone
  america/cordoba                   America/Cordoba Zone
  america/costa_rica                America/Costa_Rica Zone
  america/creston                   America/Creston Zone
  america/cuiaba                    America/Cuiaba Zone
  america/curacao                   America/Curacao Zone
  america/danmarkshavn              America/Danmarkshavn Zone
  america/dawson                    America/Dawson Zone
  america/dawson_creek              America/Dawson_Creek Zone
  america/denver                    America/Denver Zone
  america/detroit                   America/Detroit Zone
  america/dominica                  America/Dominica Zone
  america/edmonton                  America/Edmonton Zone
  america/eirunepe                  America/Eirunepe Zone
  america/el_salvador               America/El_Salvador Zone
  america/ensenada                  America/Ensenada Zone
  america/fort_wayne                America/Fort_Wayne Zone
  america/fortaleza                 America/Fortaleza Zone
  america/glace_bay                 America/Glace_Bay Zone
  america/godthab                   America/Godthab Zone
  america/goose_bay                 America/Goose_Bay Zone
  america/grand_turk                America/Grand_Turk Zone
  america/grenada                   America/Grenada Zone
  america/guadeloupe                America/Guadeloupe Zone
  america/guatemala                 America/Guatemala Zone
  america/guayaquil                 America/Guayaquil Zone
  america/guyana                    America/Guyana Zone
  america/halifax                   America/Halifax Zone
  america/havana                    America/Havana Zone
  america/hermosillo                America/Hermosillo Zone
  america/indiana/indianapolis      America/Indiana/Indianapolis Zone
  america/indiana/knox              America/Indiana/Knox Zone
  america/indiana/marengo           America/Indiana/Marengo Zone
  america/indiana/petersburg        America/Indiana/Petersburg Zone
  america/indiana/tell_city         America/Indiana/Tell_City Zone
  america/indiana/vevay             America/Indiana/Vevay Zone
  america/indiana/vincennes         America/Indiana/Vincennes Zone
  america/indiana/winamac           America/Indiana/Winamac Zone
  america/indianapolis              America/Indianapolis Zone
  america/inuvik                    America/Inuvik Zone
  america/iqaluit                   America/Iqaluit Zone
  america/jamaica                   America/Jamaica Zone
  america/jujuy                     America/Jujuy Zone
  america/juneau                    America/Juneau Zone
  america/kentucky/louisville       America/Kentucky/Louisville Zone
  america/kentucky/monticello       America/Kentucky/Monticello Zone
  america/knox_in                   America/Knox_IN Zone
  america/kralendijk                America/Kralendijk Zone
  america/la_paz                    America/La_Paz Zone
  america/lima                      America/Lima Zone
  america/los_angeles               America/Los_Angeles Zone
  america/louisville                America/Louisville Zone
  america/lower_princes             America/Lower_Princes Zone
  america/maceio                    America/Maceio Zone
  america/managua                   America/Managua Zone
  america/manaus                    America/Manaus Zone
  america/marigot                   America/Marigot Zone
  america/martinique                America/Martinique Zone
  america/matamoros                 America/Matamoros Zone
  america/mazatlan                  America/Mazatlan Zone
  america/mendoza                   America/Mendoza Zone
  america/menominee                 America/Menominee Zone
  america/merida                    America/Merida Zone
  america/metlakatla                America/Metlakatla Zone
  america/mexico_city               America/Mexico_City Zone
  america/miquelon                  America/Miquelon Zone
  america/moncton                   America/Moncton Zone
  america/monterrey                 America/Monterrey Zone
  america/montevideo                America/Montevideo Zone
  america/montreal                  America/Montreal Zone
  america/montserrat                America/Montserrat Zone
  america/nassau                    America/Nassau Zone
  america/new_york                  America/New_York Zone
  america/nipigon                   America/Nipigon Zone
  america/nome                      America/Nome Zone
  america/noronha                   America/Noronha Zone
  america/north_dakota/beulah       America/North_Dakota/Beulah Zone
  america/north_dakota/center       America/North_Dakota/Center Zone
  america/north_dakota/new_salem    America/North_Dakota/New_Salem Zone
  america/ojinaga                   America/Ojinaga Zone
  america/panama                    America/Panama Zone
  america/pangnirtung               America/Pangnirtung Zone
  america/paramaribo                America/Paramaribo Zone
  america/phoenix                   America/Phoenix Zone
  america/port-au-prince            America/Port-au-Prince Zone
  america/port_of_spain             America/Port_of_Spain Zone
  america/porto_acre                America/Porto_Acre Zone
  america/porto_velho               America/Porto_Velho Zone
  america/puerto_rico               America/Puerto_Rico Zone
  america/rainy_river               America/Rainy_River Zone
  america/rankin_inlet              America/Rankin_Inlet Zone
  america/recife                    America/Recife Zone
  america/regina                    America/Regina Zone
  america/resolute                  America/Resolute Zone
  america/rio_branco                America/Rio_Branco Zone
  america/rosario                   America/Rosario Zone
  america/santa_isabel              America/Santa_Isabel Zone
  america/santarem                  America/Santarem Zone
  america/santiago                  America/Santiago Zone
  america/santo_domingo             America/Santo_Domingo Zone
  america/sao_paulo                 America/Sao_Paulo Zone
  america/scoresbysund              America/Scoresbysund Zone
  america/shiprock                  America/Shiprock Zone
  america/sitka                     America/Sitka Zone
  america/st_barthelemy             America/St_Barthelemy Zone
  america/st_johns                  America/St_Johns Zone
  america/st_kitts                  America/St_Kitts Zone
  america/st_lucia                  America/St_Lucia Zone
  america/st_thomas                 America/St_Thomas Zone
  america/st_vincent                America/St_Vincent Zone
  america/swift_current             America/Swift_Current Zone
  america/tegucigalpa               America/Tegucigalpa Zone
  america/thule                     America/Thule Zone
  america/thunder_bay               America/Thunder_Bay Zone
  america/tijuana                   America/Tijuana Zone
  america/toronto                   America/Toronto Zone
  america/tortola                   America/Tortola Zone
  america/vancouver                 America/Vancouver Zone
  america/virgin                    America/Virgin Zone
  america/whitehorse                America/Whitehorse Zone
  america/winnipeg                  America/Winnipeg Zone
  america/yakutat                   America/Yakutat Zone
  america/yellowknife               America/Yellowknife Zone
  antarctica/casey                  Antarctica/Casey Zone
  antarctica/davis                  Antarctica/Davis Zone
  antarctica/dumontdurville         Antarctica/DumontDUrville Zone
  antarctica/macquarie              Antarctica/Macquarie Zone
  antarctica/mawson                 Antarctica/Mawson Zone
  antarctica/mcmurdo                Antarctica/McMurdo Zone
  antarctica/palmer                 Antarctica/Palmer Zone
  antarctica/rothera                Antarctica/Rothera Zone
  antarctica/south_pole             Antarctica/South_Pole Zone
  antarctica/syowa                  Antarctica/Syowa Zone
  antarctica/troll                  Antarctica/Troll Zone
  antarctica/vostok                 Antarctica/Vostok Zone
  arctic/longyearbyen               Arctic/Longyearbyen Zone
  asia/aden                         Asia/Aden Zone
  asia/almaty                       Asia/Almaty Zone
  asia/amman                        Asia/Amman Zone
  asia/anadyr                       Asia/Anadyr Zone
  asia/aqtau                        Asia/Aqtau Zone
  asia/aqtobe                       Asia/Aqtobe Zone
  asia/ashgabat                     Asia/Ashgabat Zone
  asia/ashkhabad                    Asia/Ashkhabad Zone
  asia/baghdad                      Asia/Baghdad Zone
  asia/bahrain                      Asia/Bahrain Zone
  asia/baku                         Asia/Baku Zone
  asia/bangkok                      Asia/Bangkok Zone
  asia/beirut                       Asia/Beirut Zone
  asia/bishkek                      Asia/Bishkek Zone
  asia/brunei                       Asia/Brunei Zone
  asia/calcutta                     Asia/Calcutta Zone
  asia/chita                        Asia/Chita Zone
  asia/choibalsan                   Asia/Choibalsan Zone
  asia/chongqing                    Asia/Chongqing Zone
  asia/chungking                    Asia/Chungking Zone
  asia/colombo                      Asia/Colombo Zone
  asia/dacca                        Asia/Dacca Zone
  asia/damascus                     Asia/Damascus Zone
  asia/dhaka                        Asia/Dhaka Zone
  asia/dili                         Asia/Dili Zone
  asia/dubai                        Asia/Dubai Zone
  asia/dushanbe                     Asia/Dushanbe Zone
  asia/gaza                         Asia/Gaza Zone
  asia/harbin                       Asia/Harbin Zone
  asia/hebron                       Asia/Hebron Zone
  asia/ho_chi_minh                  Asia/Ho_Chi_Minh Zone
  asia/hong_kong                    Asia/Hong_Kong Zone
  asia/hovd                         Asia/Hovd Zone
  asia/irkutsk                      Asia/Irkutsk Zone
  asia/istanbul                     Asia/Istanbul Zone
  asia/jakarta                      Asia/Jakarta Zone
  asia/jayapura                     Asia/Jayapura Zone
  asia/jerusalem                    Asia/Jerusalem Zone
  asia/kabul                        Asia/Kabul Zone
  asia/kamchatka                    Asia/Kamchatka Zone
  asia/karachi                      Asia/Karachi Zone
  asia/kashgar                      Asia/Kashgar Zone
  asia/kathmandu                    Asia/Kathmandu Zone
  asia/katmandu                     Asia/Katmandu Zone
  asia/khandyga                     Asia/Khandyga Zone
  asia/kolkata                      Asia/Kolkata Zone
  asia/krasnoyarsk                  Asia/Krasnoyarsk Zone
  asia/kuala_lumpur                 Asia/Kuala_Lumpur Zone
  asia/kuching                      Asia/Kuching Zone
  asia/kuwait                       Asia/Kuwait Zone
  asia/macao                        Asia/Macao Zone
  asia/macau                        Asia/Macau Zone
  asia/magadan                      Asia/Magadan Zone
  asia/makassar                     Asia/Makassar Zone
  asia/manila                       Asia/Manila Zone
  asia/muscat                       Asia/Muscat Zone
  asia/nicosia                      Asia/Nicosia Zone
  asia/novokuznetsk                 Asia/Novokuznetsk Zone
  asia/novosibirsk                  Asia/Novosibirsk Zone
  asia/omsk                         Asia/Omsk Zone
  asia/oral                         Asia/Oral Zone
  asia/phnom_penh                   Asia/Phnom_Penh Zone
  asia/pontianak                    Asia/Pontianak Zone
  asia/pyongyang                    Asia/Pyongyang Zone
  asia/qatar                        Asia/Qatar Zone
  asia/qyzylorda                    Asia/Qyzylorda Zone
  asia/rangoon                      Asia/Rangoon Zone
  asia/riyadh                       Asia/Riyadh Zone
  asia/saigon                       Asia/Saigon Zone
  asia/sakhalin                     Asia/Sakhalin Zone
  asia/samarkand                    Asia/Samarkand Zone
  asia/seoul                        Asia/Seoul Zone
  asia/shanghai                     Asia/Shanghai Zone
  asia/singapore                    Asia/Singapore Zone
  asia/srednekolymsk                Asia/Srednekolymsk Zone
  asia/taipei                       Asia/Taipei Zone
  asia/tashkent                     Asia/Tashkent Zone
  asia/tbilisi                      Asia/Tbilisi Zone
  asia/tehran                       Asia/Tehran Zone
  asia/tel_aviv                     Asia/Tel_Aviv Zone
  asia/thimbu                       Asia/Thimbu Zone
  asia/thimphu                      Asia/Thimphu Zone
  asia/tokyo                        Asia/Tokyo Zone
  asia/ujung_pandang                Asia/Ujung_Pandang Zone
  asia/ulaanbaatar                  Asia/Ulaanbaatar Zone
  asia/ulan_bator                   Asia/Ulan_Bator Zone
  asia/urumqi                       Asia/Urumqi Zone
  asia/ust-nera                     Asia/Ust-Nera Zone
  asia/vientiane                    Asia/Vientiane Zone
  asia/vladivostok                  Asia/Vladivostok Zone
  asia/yakutsk                      Asia/Yakutsk Zone
  asia/yekaterinburg                Asia/Yekaterinburg Zone
  asia/yerevan                      Asia/Yerevan Zone
  atlantic/azores                   Atlantic/Azores Zone
  atlantic/bermuda                  Atlantic/Bermuda Zone
  atlantic/canary                   Atlantic/Canary Zone
  atlantic/cape_verde               Atlantic/Cape_Verde Zone
  atlantic/faeroe                   Atlantic/Faeroe Zone
  atlantic/faroe                    Atlantic/Faroe Zone
  atlantic/jan_mayen                Atlantic/Jan_Mayen Zone
  atlantic/madeira                  Atlantic/Madeira Zone
  atlantic/reykjavik                Atlantic/Reykjavik Zone
  atlantic/south_georgia            Atlantic/South_Georgia Zone
  atlantic/st_helena                Atlantic/St_Helena Zone
  atlantic/stanley                  Atlantic/Stanley Zone
  australia/act                     Australia/ACT Zone
  australia/adelaide                Australia/Adelaide Zone
  australia/brisbane                Australia/Brisbane Zone
  australia/broken_hill             Australia/Broken_Hill Zone
  australia/canberra                Australia/Canberra Zone
  australia/currie                  Australia/Currie Zone
  australia/darwin                  Australia/Darwin Zone
  australia/eucla                   Australia/Eucla Zone
  australia/hobart                  Australia/Hobart Zone
  australia/lhi                     Australia/LHI Zone
  australia/lindeman                Australia/Lindeman Zone
  australia/lord_howe               Australia/Lord_Howe Zone
  australia/melbourne               Australia/Melbourne Zone
  australia/north                   Australia/North Zone
  australia/nsw                     Australia/NSW Zone
  australia/perth                   Australia/Perth Zone
  australia/queensland              Australia/Queensland Zone
  australia/south                   Australia/South Zone
  australia/sydney                  Australia/Sydney Zone
  australia/tasmania                Australia/Tasmania Zone
  australia/victoria                Australia/Victoria Zone
  australia/west                    Australia/West Zone
  australia/yancowinna              Australia/Yancowinna Zone
  brazil/acre                       Brazil/Acre Zone
  brazil/denoronha                  Brazil/DeNoronha Zone
  brazil/east                       Brazil/East Zone
  brazil/west                       Brazil/West Zone
  canada/atlantic                   Canada/Atlantic Zone
  canada/central                    Canada/Central Zone
  canada/east-saskatchewan          Canada/East-Saskatchewan Zone
  canada/eastern                    Canada/Eastern Zone
  canada/mountain                   Canada/Mountain Zone
  canada/newfoundland               Canada/Newfoundland Zone
  canada/pacific                    Canada/Pacific Zone
  canada/saskatchewan               Canada/Saskatchewan Zone
  canada/yukon                      Canada/Yukon Zone
  cet                               CET Zone
  chile/continental                 Chile/Continental Zone
  chile/easterisland                Chile/EasterIsland Zone
  cst6cdt                           CST6CDT Zone
  cuba                              Cuba Zone
  eet                               EET Zone
  egypt                             Egypt Zone
  eire                              Eire Zone
  est                               EST Zone
  est5edt                           EST5EDT Zone
  etc/gmt                           Etc/GMT Zone
  etc/gmt+0                         Etc/GMT+0 Zone
  etc/gmt+1                         Etc/GMT+1 Zone
  etc/gmt+10                        Etc/GMT+10 Zone
  etc/gmt+11                        Etc/GMT+11 Zone
  etc/gmt+12                        Etc/GMT+12 Zone
  etc/gmt+2                         Etc/GMT+2 Zone
  etc/gmt+3                         Etc/GMT+3 Zone
  etc/gmt+4                         Etc/GMT+4 Zone
  etc/gmt+5                         Etc/GMT+5 Zone
  etc/gmt+6                         Etc/GMT+6 Zone
  etc/gmt+7                         Etc/GMT+7 Zone
  etc/gmt+8                         Etc/GMT+8 Zone
  etc/gmt+9                         Etc/GMT+9 Zone
  etc/gmt-0                         Etc/GMT-0 Zone
  etc/gmt-1                         Etc/GMT-1 Zone
  etc/gmt-10                        Etc/GMT-10 Zone
  etc/gmt-11                        Etc/GMT-11 Zone
  etc/gmt-12                        Etc/GMT-12 Zone
  etc/gmt-13                        Etc/GMT-13 Zone
  etc/gmt-14                        Etc/GMT-14 Zone
  etc/gmt-2                         Etc/GMT-2 Zone
  etc/gmt-3                         Etc/GMT-3 Zone
  etc/gmt-4                         Etc/GMT-4 Zone
  etc/gmt-5                         Etc/GMT-5 Zone
  etc/gmt-6                         Etc/GMT-6 Zone
  etc/gmt-7                         Etc/GMT-7 Zone
  etc/gmt-8                         Etc/GMT-8 Zone
  etc/gmt-9                         Etc/GMT-9 Zone
  etc/gmt0                          Etc/GMT0 Zone
  etc/greenwich                     Etc/Greenwich Zone
  etc/uct                           Etc/UCT Zone
  etc/universal                     Etc/Universal Zone
  etc/utc                           Etc/UTC Zone
  etc/zulu                          Etc/Zulu Zone
  europe/amsterdam                  Europe/Amsterdam Zone
  europe/andorra                    Europe/Andorra Zone
  europe/athens                     Europe/Athens Zone
  europe/belfast                    Europe/Belfast Zone
  europe/belgrade                   Europe/Belgrade Zone
  europe/berlin                     Europe/Berlin Zone
  europe/bratislava                 Europe/Bratislava Zone
  europe/brussels                   Europe/Brussels Zone
  europe/bucharest                  Europe/Bucharest Zone
  europe/budapest                   Europe/Budapest Zone
  europe/busingen                   Europe/Busingen Zone
  europe/chisinau                   Europe/Chisinau Zone
  europe/copenhagen                 Europe/Copenhagen Zone
  europe/dublin                     Europe/Dublin Zone
  europe/gibraltar                  Europe/Gibraltar Zone
  europe/guernsey                   Europe/Guernsey Zone
  europe/helsinki                   Europe/Helsinki Zone
  europe/isle_of_man                Europe/Isle_of_Man Zone
  europe/istanbul                   Europe/Istanbul Zone
  europe/jersey                     Europe/Jersey Zone
  europe/kaliningrad                Europe/Kaliningrad Zone
  europe/kiev                       Europe/Kiev Zone
  europe/lisbon                     Europe/Lisbon Zone
  europe/ljubljana                  Europe/Ljubljana Zone
  europe/london                     Europe/London Zone
  europe/luxembourg                 Europe/Luxembourg Zone
  europe/madrid                     Europe/Madrid Zone
  europe/malta                      Europe/Malta Zone
  europe/mariehamn                  Europe/Mariehamn Zone
  europe/minsk                      Europe/Minsk Zone
  europe/monaco                     Europe/Monaco Zone
  europe/moscow                     Europe/Moscow Zone
  europe/nicosia                    Europe/Nicosia Zone
  europe/oslo                       Europe/Oslo Zone
  europe/paris                      Europe/Paris Zone
  europe/podgorica                  Europe/Podgorica Zone
  europe/prague                     Europe/Prague Zone
  europe/riga                       Europe/Riga Zone
  europe/rome                       Europe/Rome Zone
  europe/samara                     Europe/Samara Zone
  europe/san_marino                 Europe/San_Marino Zone
  europe/sarajevo                   Europe/Sarajevo Zone
  europe/simferopol                 Europe/Simferopol Zone
  europe/skopje                     Europe/Skopje Zone
  europe/sofia                      Europe/Sofia Zone
  europe/stockholm                  Europe/Stockholm Zone
  europe/tallinn                    Europe/Tallinn Zone
  europe/tirane                     Europe/Tirane Zone
  europe/tiraspol                   Europe/Tiraspol Zone
  europe/uzhgorod                   Europe/Uzhgorod Zone
  europe/vaduz                      Europe/Vaduz Zone
  europe/vatican                    Europe/Vatican Zone
  europe/vienna                     Europe/Vienna Zone
  europe/vilnius                    Europe/Vilnius Zone
  europe/volgograd                  Europe/Volgograd Zone
  europe/warsaw                     Europe/Warsaw Zone
  europe/zagreb                     Europe/Zagreb Zone
  europe/zaporozhye                 Europe/Zaporozhye Zone
  europe/zurich                     Europe/Zurich Zone
  factory                           Factory Zone
  gb                                GB Zone
  gb-eire                           GB-Eire Zone
  gmt                               GMT Zone
  gmt+0                             GMT+0 Zone
  gmt-0                             GMT-0 Zone
  gmt0                              GMT0 Zone
  greenwich                         Greenwich Zone
  hongkong                          Hongkong Zone
  hst                               HST Zone
  iceland                           Iceland Zone
  indian/antananarivo               Indian/Antananarivo Zone
  indian/chagos                     Indian/Chagos Zone
  indian/christmas                  Indian/Christmas Zone
  indian/cocos                      Indian/Cocos Zone
  indian/comoro                     Indian/Comoro Zone
  indian/kerguelen                  Indian/Kerguelen Zone
  indian/mahe                       Indian/Mahe Zone
  indian/maldives                   Indian/Maldives Zone
  indian/mauritius                  Indian/Mauritius Zone
  indian/mayotte                    Indian/Mayotte Zone
  indian/reunion                    Indian/Reunion Zone
  iran                              Iran Zone
  israel                            Israel Zone
  jamaica                           Jamaica Zone
  japan                             Japan Zone
  kwajalein                         Kwajalein Zone
  libya                             Libya Zone
  met                               MET Zone
  mexico/bajanorte                  Mexico/BajaNorte Zone
  mexico/bajasur                    Mexico/BajaSur Zone
  mexico/general                    Mexico/General Zone
  mst                               MST Zone
  mst7mdt                           MST7MDT Zone
  navajo                            Navajo Zone
  nz                                NZ Zone
  nz-chat                           NZ-CHAT Zone
  pacific/apia                      Pacific/Apia Zone
  pacific/auckland                  Pacific/Auckland Zone
  pacific/bougainville              Pacific/Bougainville Zone
  pacific/chatham                   Pacific/Chatham Zone
  pacific/chuuk                     Pacific/Chuuk Zone
  pacific/easter                    Pacific/Easter Zone
  pacific/efate                     Pacific/Efate Zone
  pacific/enderbury                 Pacific/Enderbury Zone
  pacific/fakaofo                   Pacific/Fakaofo Zone
  pacific/fiji                      Pacific/Fiji Zone
  pacific/funafuti                  Pacific/Funafuti Zone
  pacific/galapagos                 Pacific/Galapagos Zone
  pacific/gambier                   Pacific/Gambier Zone
  pacific/guadalcanal               Pacific/Guadalcanal Zone
  pacific/guam                      Pacific/Guam Zone
  pacific/honolulu                  Pacific/Honolulu Zone
  pacific/johnston                  Pacific/Johnston Zone
  pacific/kiritimati                Pacific/Kiritimati Zone
  pacific/kosrae                    Pacific/Kosrae Zone
  pacific/kwajalein                 Pacific/Kwajalein Zone
  pacific/majuro                    Pacific/Majuro Zone
  pacific/marquesas                 Pacific/Marquesas Zone
  pacific/midway                    Pacific/Midway Zone
  pacific/nauru                     Pacific/Nauru Zone
  pacific/niue                      Pacific/Niue Zone
  pacific/norfolk                   Pacific/Norfolk Zone
  pacific/noumea                    Pacific/Noumea Zone
  pacific/pago_pago                 Pacific/Pago_Pago Zone
  pacific/palau                     Pacific/Palau Zone
  pacific/pitcairn                  Pacific/Pitcairn Zone
  pacific/pohnpei                   Pacific/Pohnpei Zone
  pacific/ponape                    Pacific/Ponape Zone
  pacific/port_moresby              Pacific/Port_Moresby Zone
  pacific/rarotonga                 Pacific/Rarotonga Zone
  pacific/saipan                    Pacific/Saipan Zone
  pacific/samoa                     Pacific/Samoa Zone
  pacific/tahiti                    Pacific/Tahiti Zone
  pacific/tarawa                    Pacific/Tarawa Zone
  pacific/tongatapu                 Pacific/Tongatapu Zone
  pacific/truk                      Pacific/Truk Zone
  pacific/wake                      Pacific/Wake Zone
  pacific/wallis                    Pacific/Wallis Zone
  pacific/yap                       Pacific/Yap Zone
  poland                            Poland Zone
  portugal                          Portugal Zone
  prc                               PRC Zone
  pst8pdt                           PST8PDT Zone
  roc                               ROC Zone
  rok                               ROK Zone
  singapore                         Singapore Zone
  turkey                            Turkey Zone
  uct                               UCT Zone
  universal                         Universal Zone
  us/alaska                         US/Alaska Zone
  us/aleutian                       US/Aleutian Zone
  us/arizona                        US/Arizona Zone
  us/central                        US/Central Zone
  us/east-indiana                   US/East-Indiana Zone
  us/eastern                        US/Eastern Zone
  us/hawaii                         US/Hawaii Zone
  us/indiana-starke                 US/Indiana-Starke Zone
  us/michigan                       US/Michigan Zone
  us/mountain                       US/Mountain Zone
  us/pacific                        US/Pacific Zone
  us/samoa                          US/Samoa Zone
  utc                               UTC Zone
  w-su                              W-SU Zone
  wet                               WET Zone
  zulu                              Zulu Zone

#### Examples

```
switch(config)# timezone set us/alaska
```

### Unsetting Timezone on the switch
#### Syntax
`no timezone set *TIMEZONE*`

#### Description
This command removes the configured Timezone, and sets it to the default UTC timezone.

#### Authority
All users.

#### Parameters
This command takes in the same parameters as the "timezone set" command. Please refer above.

#### Examples
```
switch(config)#no timezone set us/alaska
```


### Showing system information
#### Syntax
`show system [ < fan | temperature [ detail ] | led | power-supply >]`

#### Description
Using no parameters, this command shows the overall system details, including information about physical components such as the fan, temperature sensor, LED, and power supply. Using a parameter, this command gives detailed information of various physical components.

#### Authority
All users.

#### Parameters
| Parameter 1 | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *fan* | choose one| Literal | Displays fan information. |
| *temperature * | choose one| Literal | Displays temperature-sensor information. |
| *led* | choose one| Literal | Displays LED information. |
| *power-supply* | choose one| Literal | Displays power-supply information. |

| Parameter 2 | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *detail* | Optional | Literal | Displays detailed temperature-sensor information. |

#### Examples
```
switch#show system
OpenSwitch Version  :
Product Name        : 5712-54X-O-AC-F
Vendor              : Edgecore
Platform            : x86_64-accton_as5712_54x-r0
Manufacturer        : Accton
Manufacturer Date   : 03/24/2015 02:05:30
Serial Number       : 571254X1512035      Label Revision      : R01H
ONIE Version        : 2014.08.00.05       DIAG Version        : 2.0.1.0
Base MAC Address    : 70:72:cf:fd:e9:b9   Number of MACs      : 74
Interface Count     : 78                  Max Interface Speed : 40000 Mbps

Fan details:
Name           Speed     Status
--------------------------------
base-1L        normal    ok
base-1R        normal    ok
base-2L        normal    ok
base-2R        normal    ok
base-3L        normal    ok
base-3R        normal    ok
base-4L        normal    ok
base-4R        normal    ok
base-5L        normal    ok
base-5R        normal    ok

LED details:

Name      State     Status
-------------------------
base-loc  on        ok
Power supply details:
Name      Status
-----------------------

base-1    ok
base-2    Input Fault
Temperature Sensors:
Location                                          Name      Reading(celsius)
---------------------------------------------------------------------------
front                                             base-1    21.00
side                                              base-3    18.00
back                                              base-2    20.00
```

### System fan information
#### Syntax
`show system fan`
#### Description
This command displays detailed fan information.
#### Authority
All users
#### Parameters
This command does not require a parameter
#### Example
```
switch#show system fan

Fan information
------------------------------------------------------
Name         Speed  Direction      Status        RPM
------------------------------------------------------
base-2L      normal front-to-back  ok            9600
base-5R      normal front-to-back  ok            8100
base-3R      normal front-to-back  ok            8100
base-4R      normal front-to-back  ok            8100
base-3L      normal front-to-back  ok            9600
base-5L      normal front-to-back  ok            9600
base-1R      normal front-to-back  ok            8100
base-1L      normal front-to-back  ok            9600
base-2R      normal front-to-back  ok            7950
base-4L      normal front-to-back  ok            9600
------------------------------------------------------
Fan speed override is not configured
------------------------------------------------------
```
### Showing system temperature information
#### Syntax
`
show system temperature [detail]
`
#### Description
This command displays detailed temperature sensor information. If a parameter is not used, the command displays minimal temperature information.

#### Authority
All users.

#### Parameters
| Parameter  | Status   | Syntax         | Description                           |
|:-----------|:----------|:----------------:|:---------------------------------------|
| *detail* | Optional | Literal | Displays detailed temperature-sensor information. |

#### Example
```
switch#show system temperature

Temperature information
---------------------------------------------------
            Current
Name      temperature    Status         Fan state
            (in C)
---------------------------------------------------
base-1    21.50          normal         normal
base-3    18.50          normal         normal
base-2    20.50          normal         normal
```
```
switch#show system temperature detail

Detailed temperature information
---------------------------------------------------
Name                      :base-1
Location                  :front
Status                    :normal
Fan-state                 :normal
Current temperature(in C) :21.50
Minimum temperature(in C) :19.50
Maximum temperature(in C) :22.00

Name                      :base-3
Location                  :side
Status                    :normal
Fan-state                 :normal
Current temperature(in C) :18.50
Minimum temperature(in C) :17.50
Maximum temperature(in C) :19.50

Name                      :base-2
Location                  :back
Status                    :normal
Fan-state                 :normal
Current temperature(in C) :20.50
Minimum temperature(in C) :18.50
Maximum temperature(in C) :21.00

```

### Showing system LED information
#### Syntax
`show system led`

#### Description
This command displays detailed LED information.

#### Authority
All users

#### Parameters
This command does not require a parameter.

#### Example
```
switch#show system led

Name           State     Status
-----------------------------------
base-loc       on        ok
```

### Showing system power-supply information

#### Syntax
`show system power-supply`

#### Description
This command displays detailed power-supply information.

#### Authority
All users.

#### Parameters
This command does not require a parameter.

#### Examples
```
switch#show system power-supply
Name           Status
-----------------------------
base-1         ok
base-2         Input Fault
```

### Showing system clock information

#### Syntax
`show system clock`

#### Description
This command displays system clock information. It shows system time in <<para>Day> <<para>Mon> <<para>Date> <<para>hh:mm:ss> <<para>timezone> <<para>year> format.

#### Authority
All users.

#### Parameters
No parameters.

#### Examples
```
switch# show system clock
  Wed Jun 22 18:39:48 UTC 2016
switch#
```

### Showing system CPU information using top

#### Syntax
`top cpu`

#### Description
This command displays detailed CPU information sorted by CPU usage.

#### Authority
All users.

#### Parameters
This command does not require a parameter.

#### Examples
```
switch# top cpu
top - 23:06:26 up 16:21,  0 users,  load average: 0.85, 0.56, 0.67
Tasks:  45 total,   1 running,  42 sleeping,   0 stopped,   2 zombie
%Cpu(s):  5.7 us,  1.2 sy,  0.0 ni, 93.0 id,  0.0 wa,  0.0 hi,  0.1 si,  0.0 st
KiB Mem : 10221884 total,  1566952 free,   853212 used,  7801720 buff/cache
KiB Swap:  8385532 total,  8368236 free,    17296 used.  9044772 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
    1 root      20   0   29996   4644   3488 S   0.0  0.0   0:00.19 /sbin/init
   16 root      20   0   23352   5796   5524 S   0.0  0.1   0:00.34 /lib/systemd/systemd-journald
   65 root      20   0   32452   2924   2492 S   0.0  0.0   0:00.02 /lib/systemd/systemd-udevd
  138 systemd+  20   0   18276   2688   2484 S   0.0  0.0   0:00.00 /lib/systemd/systemd-resolved
  142 root      20   0  259676   2936   2588 S   0.0  0.0   0:00.06 /usr/sbin/rsyslogd -n
  150 message+  20   0   13180   2496   2272 S   0.0  0.0   0:00.00 /usr/bin/dbus-daemon --system +
  151 root      20   0   13108   2352   2144 S   0.0  0.0   0:00.00 /lib/systemd/systemd-logind
  153 root      20   0   15712   2216   1652 S   0.0  0.0   0:00.00 /usr/sbin/crond -n
```

### Showing system memory information using top

#### Syntax
`top memory`

#### Description
This command displays detailed memory information sorted by memory usage.

#### Authority
All users.

#### Parameters
This command does not require a parameter.

#### Examples
```
switch# top memory
top - 23:08:08 up 16:23,  0 users,  load average: 0.32, 0.45, 0.62
Tasks:  45 total,   1 running,  42 sleeping,   0 stopped,   2 zombie
%Cpu(s):  5.7 us,  1.2 sy,  0.0 ni, 93.1 id,  0.0 wa,  0.0 hi,  0.1 si,  0.0 st
KiB Mem : 10221884 total,  1546164 free,   873572 used,  7802148 buff/cache
KiB Swap:  8385532 total,  8368236 free,    17296 used.  9024352 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
  321 root      20   0  161984  38516   8848 S   0.0  0.4   0:02.75 python /usr/bin/restd
  236 root      20   0  182212  18520   7176 S   0.0  0.2   0:00.81 python /usr/bin/ops_ntpd
  253 root      20   0  101828  18052   7108 S   0.0  0.2   0:00.29 python /usr/bin/ops_dhcp_tftp
  312 root      20   0  112496  17312   3992 S   0.0  0.2   0:00.07 python /usr/bin/ops_mgmtintfcf+
  405 root      20   0  109908  16208   3344 S   0.0  0.2   0:00.66 python /usr/bin/ops_ntpd
  313 root      20   0  101564  14008   3244 S   0.0  0.1   0:00.00 python /usr/bin/ops_aaautilspa+
  188 root      20   0   40288  13300   4636 S   0.0  0.1   0:00.35 /usr/sbin/ovsdb-server --remot+
```
### Showing Timezone information

#### Syntax
`show system timezone`

#### Description
This command displays detailed information for the Timezone configured on the system.

#### Authority
All users

#### Parameters
This command does not require a parameter

#### Example
By default the timezone configured should be UTC.
```
switch# show system timezone
System is configured for timezone : UTC
      DST active: n/a
```
If we configure a timezone of "US/Alaska", then we should be able to verify using 'show system timezone' 
```
switch# show system timezone
System is configured for timezone : US/Alaska
      DST active: yes
 Last DST change: DST began at
                  Sun 2016-03-13 01:59:59 AKST
                  Sun 2016-03-13 03:00:00 AKDT
 Next DST change: DST ends (the clock jumps one hour backwards) at
                  Sun 2016-11-06 01:59:59 AKDT
                  Sun 2016-11-06 01:00:00 AKST
```

