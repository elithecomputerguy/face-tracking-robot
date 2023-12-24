#define left_forward 3
#define left_backward 5
#define right_forward 6
#define right_backward 9

String command;

void setup() {

  Serial.begin(9600);
  Serial.println("Type Command (forward=f, backward=b, left=l, right=r, stop=s)");

  pinMode(left_forward, OUTPUT);
  pinMode(left_backward, OUTPUT);
  pinMode(right_forward, OUTPUT);
  pinMode(right_backward, OUTPUT);

  delay(2000);

}

void loop() {

  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();

    //Forward
    if (command.equals("f")) {
      digitalWrite(left_forward, HIGH);
      digitalWrite(left_backward, LOW);
      digitalWrite(right_forward, HIGH);
      digitalWrite(right_backward, LOW);
    }

    //backward
    if (command.equals("b")) {
      digitalWrite(left_forward, LOW);
      digitalWrite(left_backward, HIGH);
      digitalWrite(right_forward, LOW);
      digitalWrite(right_backward, HIGH);
    }

    //left
    if (command.equals("l")) {
      digitalWrite(left_forward, LOW);
      digitalWrite(left_backward, HIGH);
      digitalWrite(right_forward, HIGH);
      digitalWrite(right_backward, LOW);
    }

    //right
    if (command.equals("r")) {
      digitalWrite(left_forward, HIGH);
      digitalWrite(left_backward, LOW);
      digitalWrite(right_forward, LOW);
      digitalWrite(right_backward, HIGH);
    }

    //Stop
    if (command.equals("s")) {
      digitalWrite(left_forward, LOW);
      digitalWrite(left_backward, LOW);
      digitalWrite(right_forward, LOW);
      digitalWrite(right_backward, LOW);
    }
  }
}
