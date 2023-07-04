function getR0Value () {
    sensorValue = sensorValue / 100
    sensorVoltage = sensorValue / 1024 * 5
    rsValue = (5 - sensorVoltage) / sensorVoltage
    return rsValue / 60
}
let r0Value = 0
let rsValue = 0
let sensorVoltage = 0
let sensorValue = 0
let bloodAlcoholC = 0
let ratio = 0
serial.redirectToUSB()
basic.forever(function () {
    for (let index = 0; index < 100; index++) {
        sensorValue += pins.analogReadPin(AnalogPin.P1)
    }
    sensorValue = sensorValue / 100
    sensorVoltage = sensorValue / 1024 * 5
    rsValue = (5 - sensorVoltage) / sensorVoltage
    r0Value = getR0Value()
    ratio = rsValue / r0Value
    // BAC in mg/L
    bloodAlcoholC = 0.1896*ratio^2;
basic.pause(100)
    serial.writeLine("")
    serial.writeNumber(bloodAlcoholC)
    serial.writeString(" mg/L")
})
