let forrige = 0
let gass = 0
serial.redirectToUSB()
basic.forever(function () {
    gass = pins.analogReadPin(AnalogPin.P1)
    if (forrige != gass) {
        serial.writeLine("")
        serial.writeNumber(gass)
    }
    forrige = gass
})
