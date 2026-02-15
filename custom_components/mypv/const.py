"""Constants for the MYPV piko integration."""

from dataclasses import dataclass
from datetime import timedelta

from homeassistant.const import (
    PERCENTAGE,
    Platform,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)

DOMAIN = "mypv"

PLATFORMS = [Platform.SENSOR, Platform.SWITCH]

DATA_COORDINATOR = "coordinator"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)

# short name . long name
MYPV_DEVICES = {
    "AC ELWA-E": "elwa",
    "AC-THOR": "acthor",
    "AC-THOR 9s": "actor9s",
    "AC ELWA 2": "elwa2",
    "dc_elwa": "dc_elwa",
    "Wi-Fi Meter": "meter",
    "Solthor": "solthor",
    "heathorIoT 9": "heathorIot9",
    "heathorIoT 35": "heathorIot35",
    "AC-THOR32": "acthor32",
    "AC-THOR32 9s": "acthor329s",
}
# short name
MYPV_SWITCHES = [
    "devmode",
    "bstmode",
    "legmode",
    "cloudmode",
]


@dataclass
class S:
    """Sensor description with metadata for MYPV integration."""

    name_long: str
    unit: str = ""
    icon: str = ""
    device: str = ""
    source: str = "data"


# sensor_type: [name, unit, icon, page, devices]
SENSOR_TYPES = {
    "device": S("Device", device="elwa"),
    "acthor9s": S("Acthor 9s"),
    "fwversion": S("Firmware Version", icon="mdi:numeric", device="elwa"),
    "psversion": S("Power Supply Version", icon="mdi:numeric"),
    "p9sversion": S("Power Supply Version Acthor 9", icon="mdi:numeric"),
    "screen_mode_flag": S("Screen Mode"),
    "status": S(
        "Status ID",
        device="elwa acthor acthor9s acthor32 acthor329s elwa2 solthor heathorIot9 heathorIot35",
    ),
    "power": S(
        "Aktueller Verbrauch",
        UnitOfPower.WATT,
        "mdi:lightning-bolt",
        device="elwa solthor",
    ),
    "power_act": S(
        "Power AC-Thor", UnitOfPower.WATT, "mdi:lightning-bolt", device="acthor"
    ),
    "power_ac9": S(
        "Power Acthor 9", UnitOfPower.WATT, "mdi:lightning-bolt", device="acthor9s"
    ),
    "power_elwa2": S(
        "Power ELWA 2", UnitOfPower.WATT, "mdi:lightning-bolt", device="elwa2"
    ),
    "boostpower": S(
        "Warmwassersicherstellung",
        UnitOfPower.WATT,
        "mdi:thermometer-lines",
        device="elwa dc_elwa",
    ),
    "power_solar": S(
        "Solaranteil",
        UnitOfPower.WATT,
        "mdi:solar-power-variant",
        device="acthor acthor9s acthor32 acthor329s elwa2 solthor",
    ),
    "power_grid": S(
        "Netzanteil",
        UnitOfPower.WATT,
        "mdi:solar-power-variant",
        device="acthor acthor9s acthor32 acthor329s elwa2 solthor heathorIot9 heathorIot35",
    ),
    "power_L1": S("Leistung L1", UnitOfPower.WATT, device="heathorIot9 heathorIot35"),
    "power_L2": S("Leistung L2", UnitOfPower.WATT, device="heathorIot9"),
    "power_L3": S("Leistung L3", UnitOfPower.WATT, device="heathorIot9"),
    "power_solar_act": S(
        "Power from solar", UnitOfPower.WATT, "mdi:solar-power-variant"
    ),
    "power_grid_act": S(
        "Power from grid", UnitOfPower.WATT, "mdi:transmission-tower-export"
    ),
    "power_solar_ac9": S(
        "Power from solar Acthor 9", UnitOfPower.WATT, "mdi:solar-power-variant"
    ),
    "power_grid_ac9": S(
        "Power from grid Acthor 9", UnitOfPower.WATT, "mdi:transmission-tower-export"
    ),
    "power1_solar": S(
        "power1_solar",
        UnitOfPower.WATT,
        "mdi:solar-power-variant",
        device="acthor acthor9s acthor32 acthor329s elwa2",
    ),
    "power1_grid": S(
        "power1_grid",
        UnitOfPower.WATT,
        "mdi:transmission-tower-export",
        device="acthor acthor9s acthor32 acthor329s elwa2",
    ),
    "power2_solar": S(
        "power2_solar",
        UnitOfPower.WATT,
        "mdi:solar-power-variant",
        device="acthor acthor9s acthor32 acthor329s elwa2",
    ),
    "power2_grid": S(
        "power2_grid",
        UnitOfPower.WATT,
        "mdi:transmission-tower-export",
        device="acthor acthor9s acthor32 acthor329s elwa2",
    ),
    "power3_solar": S(
        "power3_solar", UnitOfPower.WATT, "mdi:solar-power-variant", device="acthor9s"
    ),
    "power3_grid": S(
        "power3_grid",
        UnitOfPower.WATT,
        "mdi:transmission-tower-export",
        device="acthor9s",
    ),
    "load_state": S("load_state", device="acthor acthor9s acthor32 acthor329s"),
    "load_nom": S(
        "load_nom", UnitOfPower.WATT, device="acthor acthor9s acthor32 acthor329"
    ),
    "rel1_out": S(
        "rel1_out",
        icon="mdi:electric-switch",
        device="acthor acthor9s acthor32 acthor329s elwa2",
    ),
    "rel_selv": S("SELV Relais Status", device="elwa2 heathorIot35 heathorIot9"),
    "ww1target": S(
        "Zieltempertaur",
        UnitOfTemperature.CELSIUS,
        "mdi:thermometer-auto",
        device="elwa",
    ),
    "temp1": S(
        "Wassertemperatur",
        UnitOfTemperature.CELSIUS,
        "mdi:thermometer-water",
        device="acthor acthor9s acthor32 acthor329s elwa elwa2 dc_elwa solthor heathorIot35 heathorIot9",
    ),
    "temp2": S(
        "Temperatur 2",
        UnitOfTemperature.CELSIUS,
        "mdi:thermometer",
        device="cthor acthor9s acthor32 acthor329s elwa2 solthor heathorIot35 heathorIot9",
    ),
    "temp3": S(
        "Temperatur 3",
        UnitOfTemperature.CELSIUS,
        "mdi:thermometer",
        device="acthor acthor9s acthor32 acthor329s solthor",
    ),
    "temp4": S(
        "Temperatur 4",
        UnitOfTemperature.CELSIUS,
        "mdi:thermometer",
        device="acthor acthor9s acthor32 acthor329s",
    ),
    "boostactive": S(
        "Boost aktiv",
        icon="mdi:thermometer-chevron-up",
        device="acthor acthor9s acthor32 acthor329s elwa elwa2 dc_elwa solthor heathorIot35 heathorIot9",
    ),
    "legboostnext": S(
        "Nächster Legionellen Boost",
        UnitOfTime.DAYS,
        "mdi:bacteria",
        device="elwa acthor acthor9s acthor32 acthor329s elwa2 heathorIot35 heathorIot9",
    ),
    "date": S("Date", icon="mdi:calendar-today"),
    "loctime": S("Lokale Uhrzeit", icon="mdi:home-clock", device="elwa"),
    "unixtime": S("Unix time", icon="mdi:web-clock", device="elwa"),
    "wp_flag": S("wp_flag"),
    "wp_time1_ctr": S("wp_time1_ctr"),
    "wp_time2_ctr": S("wp_time2_ctr"),
    "wp_time3_ctr": S("wp_time3_ctr"),
    "pump_pwm": S(
        "Pump PWM", icon="mdi:pump", device="acthor acthor9s acthor32 acthor329s"
    ),
    "schicht_flag": S("Schicht"),
    "act_night_flag": S("Night flag"),
    "ctrlstate": S(
        "Status Ansteuerung", device="elwa acthor acthor9s acthor32 acthor329s elwa2"
    ),
    "blockactive": S(
        "Block active", device="acthor acthor9s acthor32 acthor329s elwa elwa2 dc_elwa"
    ),
    "error_state": S("Error state", icon="mdi:alert-circle"),
    "meter1_id": S("my-PV Meter 1 ID", icon="mdi:identifier", device="elwa"),
    "meter1_ip": S("my-PV Meter 1 IP", icon="mdi:ip-network", device="elwa"),
    "meter2_id": S("my-PV Meter 2 ID", icon="mdi:identifier", device="elwa"),
    "meter2_ip": S("my-PV Meter 2 IP", icon="mdi:ip-network", device="elwa"),
    "meter3_id": S("my-PV Meter 3 ID", icon="mdi:identifier", device="elwa"),
    "meter3_ip": S("my-PV Meter 3 IP", icon="mdi:ip-network", device="elwa"),
    "meter4_id": S("my-PV Meter 4 ID", icon="mdi:identifier", device="elwa"),
    "meter4_ip": S("my-PV Meter 4 IP", icon="mdi:ip-network", device="elwa"),
    "meter5_id": S("my-PV Meter 5 ID", icon="mdi:identifier", device="elwa"),
    "meter5_ip": S("my-PV Meter 5 IP", icon="mdi:ip-network", device="elwa"),
    "meter6_id": S("my-PV Meter 6 ID", icon="mdi:identifier", device="elwa"),
    "meter6_ip": S("my-PV Meter 6 IP", icon="mdi:ip-network", device="elwa"),
    "meter_ss": S(
        "WiFi Meter Signalstärke",
        PERCENTAGE,
        "mdi:wifi",
        device="elwa elwa_min00205 acthor acthor_min00208 acthor9s acthor9s_min00208 elwa2",
    ),
    "meter_ssid": S(
        "WiFi Meter SSID",
        icon="mdi:wifi-marker",
        device="elwa elwa_min00205 acthor acthor_min00208 acthor9s acthor9s_min00208 elwa2",
    ),
    "surplus": S(
        "Meter + Batterieladeleistung",
        UnitOfPower.WATT,
        "mdi:lightning-bolt",
        device="elwa",
    ),
    "m0sum": S(
        "Hausanschluss", UnitOfPower.WATT, "mdi:transmission-tower", device="elwa"
    ),
    "m0l1": S(
        "Hausanschluss L1", UnitOfPower.WATT, "mdi:transmission-tower", device="elwa"
    ),
    "m0l2": S(
        "Hausanschluss L2", UnitOfPower.WATT, "mdi:transmission-tower", device="elwa"
    ),
    "m0l3": S(
        "Hausanschluss L3", UnitOfPower.WATT, "mdi:transmission-tower", device="elwa"
    ),
    "m0bat": S(
        "Batteriespeicher", UnitOfPower.WATT, "mdi:transmission-tower", device="elwa"
    ),
    "m1sum": S("PV Leistung", UnitOfPower.WATT, "mdi:solar-power", device="elwa"),
    "m1l1": S("PV Leistung L1", UnitOfPower.WATT, "mdi:solar-power", device="elwa"),
    "m1l2": S("PV Leistung L2", UnitOfPower.WATT, "mdi:solar-power", device="elwa"),
    "m1l3": S("PV Leistung L3", UnitOfPower.WATT, "mdi:solar-power", device="elwa"),
    "m1devstate": S("PV Kommunikationsstatus", icon="mdi:link", device="elwa"),
    "m2sum": S(
        "Batterie Leistung", UnitOfPower.WATT, "mdi:home-battery", device="elwa"
    ),
    "m2l1": S(
        "Batterie Leistung L1", UnitOfPower.WATT, "mdi:home-battery", device="elwa"
    ),
    "m2l2": S(
        "Batterie Leistung L2", UnitOfPower.WATT, "mdi:home-battery", device="elwa"
    ),
    "m2l3": S(
        "Batterie Leistung L3", UnitOfPower.WATT, "mdi:home-battery", device="elwa"
    ),
    "m2soc": S("Batterie SoC", PERCENTAGE, "mdi:battery-charging-50", device="elwa"),
    "m2state": S("Batterie Status", icon="mdi:battery-heart-variant", device="elwa"),
    "m2devstate": S("Batterie Kommunikationsstatus", icon="mdi:link"),
    "m3sum": S(
        "Ladestation Leistung", UnitOfPower.WATT, "mdi:ev-station", device="elwa"
    ),
    "m3l1": S("Ladestation L1", UnitOfPower.WATT, "mdi:ev-station", device="elwa"),
    "m3l2": S("Ladestation L2", UnitOfPower.WATT, "mdi:ev-station", device="elwa"),
    "m3l3": S("Ladestation L2", UnitOfPower.WATT, "mdi:ev-station", device="elwa"),
    "m3soc": S("Ladestation SoC", PERCENTAGE, "mdi:battery-charging-50", device="elwa"),
    "m3devstate": S("Ladestation Kommunikationsstatus", icon="mdi:link", device="elwa"),
    "m4sum": S("Wärmepumpe Leistung", UnitOfPower.WATT, "mdi:heat-pump", device="elwa"),
    "m4l1": S("Wärmepumpe L1", UnitOfPower.WATT, "mdi:heat-pump", device="elwa"),
    "m4l2": S("Wärmepumpe L2", UnitOfPower.WATT, "mdi:heat-pump", device="elwa"),
    "m4l3": S("Wärmepumpe L3", UnitOfPower.WATT, "mdi:heat-pump", device="elwa"),
    "m4devstate": S("Wärmepumpe Kommunikationsstatus", icon="mdi:link", device="elwa"),
    "ecarstate": S("E-Auto Status", icon="mdi:car-electric", device="elwa"),
    "ecarboostctr": S("ecarboostctr", device="elwa"),
    "mss2": S(
        "Sekundärregler 2 Status", device="acthor acthor9s acthor32 acthor329s elwa2"
    ),
    "mss3": S(
        "Sekundärregler 3 Status", device="acthor acthor9s acthor32 acthor329s elwa2"
    ),
    "mss4": S(
        "Sekundärregler 4 Status", device="acthor acthor9s acthor32 acthor329s elwa2"
    ),
    "mss5": S(
        "Sekundärregler 5 Status", device="acthor acthor9s acthor32 acthor329s elwa2"
    ),
    "mss6": S(
        "Sekundärregler 6 Status", device="acthor acthor9s acthor32 acthor329s elwa2"
    ),
    "mss7": S(
        "Sekundärregler 7 Status", device="acthor acthor9s acthor32 acthor329s elwa2"
    ),
    "mss8": S(
        "Sekundärregler 8 Status", device="acthor acthor9s acthor32 acthor329s elwa2"
    ),
    "mss9": S(
        "Sekundärregler 9 Status", device="acthor acthor9s acthor32 acthor329s elwa2"
    ),
    "mss10": S(
        "Sekundärregler 10 Status", device="acthor acthor9s acthor32 acthor329s elwa2"
    ),
    "mss11": S(
        "Sekundärregler 11 Status", device="acthor acthor9s acthor32 acthor329s elwa2"
    ),
    "tempchip": S("tempchip", UnitOfTemperature.CELSIUS, "mdi:chip", device="elwa"),
    "volt_mains": S(
        "Eingangsspannung Leistungsteil L1",
        UnitOfElectricPotential.VOLT,
        "mdi:flash-triangle",
        device="acthor acthor9s acthor32 acthor329s elwa2 solthor",
    ),
    "curr_mains": S(
        "Netzstrom L1",
        UnitOfElectricCurrent.AMPERE,
        "mdi:current-ac",
        device="acthor acthor9s acthor32 acthor329s solthor",
    ),
    "volt_mains_L1": S(
        "Eingangsspannung Leistungsteil L1",
        UnitOfElectricPotential.VOLT,
        "mdi:flash-triangle",
        device="acthor acthor9s acthor32 acthor329s elwa2 solthor",
    ),
    "curr_L1": S(
        "Current L1",
        UnitOfElectricCurrent.AMPERE,
        "mdi:current-ac",
        device="heathorIot35 heathorIot9",
    ),
    "volt_mains_L2": S(
        "Eingangsspannung Leistungsteil L2",
        UnitOfElectricPotential.VOLT,
        "mdi:flash-triangle",
        device="heathorIot9",
    ),
    "volt_L2": S(
        "Eingangsspannung Leistungsteil L2",
        UnitOfElectricPotential.VOLT,
        "mdi:flash-triangle",
        device="acthor9s",
    ),
    "curr_L2": S(
        "Current L2",
        UnitOfElectricCurrent.AMPERE,
        "mdi:current-ac",
        device="heathorIot9 acthor9s",
    ),
    "volt_mains_L3": S(
        "Eingangsspannung Leistungsteil L3",
        UnitOfElectricPotential.VOLT,
        "mdi:flash-triangle",
        device="heathorIot9",
    ),
    "volt_L3": S(
        "Eingangsspannung Leistungsteil L3",
        UnitOfElectricPotential.VOLT,
        "mdi:flash-triangle",
        device="acthor9s",
    ),
    "curr_L3": S(
        "Current L3",
        UnitOfElectricCurrent.AMPERE,
        "mdi:current-ac",
        device="heathorIot9 acthor9s",
    ),
    "volt_out": S(
        "Ausgangsspannung Leistungsteil",
        UnitOfElectricPotential.VOLT,
        "mdi:flash-triangle",
        device="acthor acthor9s acthor32 acthor329s",
    ),
    "volt_aux": S(
        "Spannung L2 an AUX-Relais",
        UnitOfElectricPotential.VOLT,
        "mdi:flash-triangle",
        device="elwa2",
    ),
    "freq": S(
        "Netzfrequenz",
        UnitOfFrequency.HERTZ,
        "mdi:sine-wave",
        device="acthor acthor9s acthor32 acthor329s elwa2 solthor heathorIot35 heathorIot9",
    ),
    "temp_ps": S(
        "Temperatur Leistungsteil",
        UnitOfTemperature.CELSIUS,
        "mdi:thermometer",
        device="acthor acthor9s acthor32 acthor329s elwa2 solthor heathorIot35 heathorIot9",
    ),
    "fan_speed": S(
        "Lüfterstufe",
        icon="mdi:fan",
        device="acthor acthor9s acthor32 acthor329s elwa2",
    ),
    "ps_state": S(
        "Status Leistungsteil", device="acthor acthor9s acthor32 acthor329s elwa2"
    ),
    "relay_boost": S("Relais Boost", device="solthor"),
    "relay_alarm": S("Relais Alarm", device="solthor"),
    "cur_ip": S("Current IP", icon="mdi:ip-network", device="elwa"),
    "cur_sn": S("Current subnet mask", icon="mdi:numeric", device="elwa"),
    "cur_gw": S("Current gateway", icon="mdi:router-network", device="elwa"),
    "cur_dns": S("Current DNS", icon="mdi:dns", device="elwa"),
    "fwversionlatest": S("latest Firmware version", icon="mdi:numeric"),
    "psversionlatest": S("latest Power supply version", icon="mdi:numeric"),
    "p9sversionlatest": S("latest Power supply version Acthor 9", icon="mdi:numeric"),
    "upd_state": S("Update state", icon="mdi:update"),
    "upd_files_left": S("Update files left", icon="mdi:update"),
    "ps_upd_state": S("Power supply update state", icon="mdi:update"),
    "p9s_upd_state": S("Acthor 9 Power supply update state", icon="mdi:update"),
    "cloudstate": S(
        "Cloud Status",
        icon="mdi:cloud-check",
        device="elwa elwa_min00201 acthor acthor_min00201 acthor9s acthor9s_min00201 elwa2 solthor heathorIot35 heathorIot9",
    ),
    "debug_ip": S(
        "Debug IP",
        icon="mdi:ip-network",
        device="elwa elwa_min00201 acthor acthor_min00201 acthor9s acthor9s_min00201 elwa2",
    ),
    "cur_eth_mode": S(
        "Ethernet-Modus", device="elwa2 solthor heathorIot35 heathorIot9"
    ),
    # setup values
    "devmode": S("Device State", source="setup", icon="mdi:power", device="elwa"),
    "bstmode": S(
        "Hot Water Boost Mode",
        source="setup",
        icon="mdi:thermometer-lines",
        device="elwa",
    ),
    "legmode": S(
        "Legionella Protection",
        source="setup",
        icon="mdi:bacteria-outline",
        device="elwa",
    ),
    "cloudmode": S("Cloud Mode", source="setup", device="elwa"),
}
