let sensor_volt = 0; 
let RS = 0;             // Get the value of RS via in a clear air
let R0 = 0;             // Get the value of R0 via in Alcohol
let sensorValue = 0;

function onButtonPressedA() {
    basic.showString("Volt:");
    basic.showNumber(sensor_volt);
}

input.onButtonPressed(Button.A, onButtonPressedA);

function onButtonPressedB() {
    basic.showString("R0 =");
    basic.showNumber(R0);
}

input.onButtonPressed(Button.B, onButtonPressedB);

basic.forever(function () {
    for (let i = 0; i < 100; i++) {
        sensorValue += pins.analogReadPin(AnalogPin.P1);
    }
    basic.pause(10);
    sensorValue = sensorValue / 100.0;    // get average of reading
    sensor_volt = sensorValue / (1024 * 5.0);

    RS = (5.0 - sensor_volt) / sensor_volt;
    R0 = RS / 50.0;                       // 50 is found using interpolation from the graph

    sensorValue = 0;
});
basic.forever(function () {
	
})