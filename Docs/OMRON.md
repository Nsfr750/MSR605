```
Printed on Oct 8, ’
```
## Data Transmission Specifications

## 3S4YR-MVFW(DL)-0** Series

## Hybrid Card Reader/Writer

```
Rev. A0 Jun. 6, 1997
Rev. A1 Aug. 28, 1997
Rev. A2 Jul. 8, 1998
Rev. A3 Jun. 7, 1999
Rev. A4 Oct. 8, 1999
```
## Card Business Promotion Division

## © OMRON Corporation 1997-

## All Rights Reserved.

# O M R O N


## i

```
Table of Contents
```
I. Introduction I
II. Applicable Card Reader/Writer I
III. Applicable CPU/FW I
IV. Reference Standards II
V. Notice for IC card (ICC) III
VI. Character Code Expression Method III

### 1.1 Basic Transmission Specifications 1-

### 1.2 Transmission Control Method 1-

### 1.3 Transmission Control Codes 1-

## 2 Time Chart of Transmission Control Signal Line 2-

### 2.1 DTR Signal 2-

### 2.2 Transmission Interruption by the CTS Signal 2-

## 3 Message Specifications 3-

### 3.1 Command Format (HOST -> C/R) 3-

### 3.2 Response Format (C/R -> HOST) 3-

#### 3.2.1 Positive Response Format 3-

#### 3.2.2 Negative Response Format 3-

## 4 Command Parameters 4-

### 4.1 Initial Setting Data (0~2 bytes) 4-

### 4.2 Track Number A (1 byte) 4-

### 4.3 Track Number B (1 byte) 4-

### 4.4 Magnetic data A (1~104 bytes ) 4-

### 4.5 Magnetic Data B (2~105 bytes) 4-


## 5 Response Data 5-

### 5.1 Sensor Information (12 bytes) 5-

### 5.2 Magnetic Data D (1~104 bytes) 5-

### 5.3 Magnetic Data E (2~105 bytes) 5-

### 5.4 Magnetic data F (6 ~233 bytes ) 5-

### 5.5 Error Track Number (0~1 byte) 5-

### 5.6 Captured Number of Card(s) (3 bytes) 5-

### 5.7 Sensor voltage Information (16 bytes) 5-

- 1 Transmission Specifications 1- VII. Definition of Terminology III
   - 1.1 Basic Transmission Specifications 1-
   - 1.2 Transmission Control Method 1-
   - 1.3 Transmission Control Codes 1-
   - 1.4 Message Format 1-
   - 1.5 Transmission Control Procedure 1-
      - 1.5.1 Transmission beginning 1-
      - 1.5.2 Normal Operation Sequence 1-
      - 1.5.3 Recovery Operation Sequence 1-
      - 1.5.4 Interruption of Transmission and Command to the C/R from the HOST. 1-
   - 1.6 Transmission Control Matrix 1-
- 2 Time Chart of Transmission Control Signal Line 2-
   - 2.1 DTR Signal 2-
   - 2.2 Transmission Interruption by the CTS Signal 2-
- 3 Message Specifications 3-
   - 3.1 Command Format (HOST -> C/R) 3-
   - 3.2 Response Format (C/R -> HOST) 3-
      - 3.2.1 Positive Response Format 3-
      - 3.2.2 Negative Response Format 3-
   - 3.3 Table of Commands 3-
      - 3.3.1 Card Reader Control Commands (RCC) 3-
      - 3.3.2 ICC Control Commands (ICC) 3-
      - 3.3.3 Table of Command related Down Load (DLC) 3-
   - 3.4 Table of Responses 3-
      - 3.4.1 Status Table of Positive Response 3-
      - 3.4.2 Status Table of Negative Response (Error Code) 3-
- 4 Command Parameters 4-
   - 4.1 Initial Setting Data (0~2 bytes) 4-
   - 4.2 Track Number A (1 byte) 4-
   - 4.3 Track Number B (1 byte) 4-
   - 4.4 Magnetic data A (1~104 bytes ) 4-
   - 4.5 Magnetic Data B (2~105 bytes) 4-
   - 4.6 Magnetic Data C (2~105 bytes) 4-
   - 4.7 Retry Number (1 byte) 4-
   - 4.8 Return Retry Number ( 2 bytes) 4-
   - 4.9 Monitoring Time Data (2 bytes) 4-
   - 4.10 P/F Condenser Existence (1 byte) 4-
   - 4.11 Magnetic head type ( 3 bytes ) 4-
   - 4.12 I/O ports using (1 byte) 4-
   - 4.13 Execution Designation Data (1 byte) 4-
   - 4.14 Transmission Format of Magnetic Data (1 byte) 4-
   - 4.15 Magnetic Format (7 bytes) 4-
   - 4.16 Start Sentinel (SS) Positioning Data (3 bytes) 4-
   - 4.17 Node Address (0 or 2 byte) 4-
   - 4.18 PTS/NAD setting (1 or 3 bytes) 4-
   - 4.19 T=0 (Character Transmission Type) Transmission Data ( 4-261 bytes ) 4-
   - 4.20 T=1(Block Transmission Type) Transmission Data (4~360 bytes) 4-
   - 4.21 T=1(Block Transmission Type) Extended Transmission Data (5~360 bytes) 4-
   - 4.22 Protocol type of PTS (1 byte) 4-
   - 4.23 The Number of Down load Block ( 23 bytes ) 4- ii
   - 4.24 Down load Data ( 2054 bytes ) 4-
   - 4.25 Output port setting (2~16 bytes) 4-
   - 4.26 Memory size of “USER” information ( 3 bytes ) 4-
   - 4.27 Output port setting time ( 4~30 bytes) 4-
   - 4.28 ICC Reference Standard(2 bytes) 4-
   - 4.29 Timer Value for Waiting for Reception (2 bytes) 4-
   - 4.30 IFSD Control Method(1 byte) 4-
   - 4.31 TCK Control Method(1 byte) 4-
   - 4.32 ICC Control Setting (8 bytes) 4-
- 5 Response Data 5-
   - 5.1 Sensor Information (12 bytes) 5-
   - 5.2 Magnetic Data D (1~104 bytes) 5-
   - 5.3 Magnetic Data E (2~105 bytes) 5-
   - 5.4 Magnetic data F (6 ~233 bytes ) 5-
   - 5.5 Error Track Number (0~1 byte) 5-
   - 5.6 Captured Number of Card(s) (3 bytes) 5-
   - 5.7 Sensor voltage Information (16 bytes) 5-
   - 5.8 Option Information (16 bytes) 5-
   - 5.9 Version Information (40 bytes) 5-
   - 5.10 ATR (Answer to Reset) Information (2~33 bytes) 5-
   - 5.11 ATR/PTS Information(3~34 bytes) 5-
   - 5.12 T=0 ( Character Transmission Type ) Reception Data ( 2~258 bytes) 5-
   - 5.13 T=1 ( Block Transmission Type) Reception Data (2~320 bytes) 5-
   - 5.14 PTS Information (1 byte) 5-
   - 5.15 Memory Version Information (22 bytes) 5-
   - 5.16 USER Information in memory (1~256 bytes) 5-
   - 5.17 Input port Information ( 4bytes) 5-
   - 5.18 FW Version Information of Nonvolatile Memory(22 bytes) 5-
   - 5.19 ICC Control Information(16 bytes) 5-


```
iii
```
[ Specification History of Modification ]

```
Rev. Date Page Content
A0 Jun. 6, 97 -- Draft
I Adds Applicable Card Reader/Writer
3-3 Adds notice of *6 (“90”)
3-4 Changes “P0” to deactivate and “P1” to activation.
4-6 Erases default value of 4.20 ( PTS/NAD setting ).
E-1 Adds using restriction of DL matrix.
```
```
A1 Aug. 28, 97
```
```
H-1 Adds Annex H (The Commands Which Can be Transmitted When
Incomplete Program)
A2 Jul. 8, 98 1,A Changes character waiting timer from 15ms to 100ms.
I Adds the applicable CPU and FW.
II Adds EMV 3.0, Errata 1.0 and EMV 3.1.1 in reference standards table.
3-4,4-8,
5-
```
```
Adds requirement of various ICC standard. (Adds ICC Control
Information and Version read of ICC control part commands.)
3-4 Delete “after the time-out.” in the explanation of “C40”, “C41” and “C42”.
3-4 Changes the positions of *1 to “Q1”,”N1”,”N2”,”N3” and “NA”.
3-5 Changes the function of “6L” from “to Front” to “to Rear End”.
3-6,4-
C-
```
```
Deletes ICC setting commands(“CB”) and command parameters.
```
```
3-12 Changes Error code table(8/8).
4-2 Changes Return Retry Number from 4 times to 3 times.
4-8,5-5 Adds “Europay” in ICC reference standard
```
```
A3 Jun. 7, 99
```
```
5-1 Adds “3” in the parameter of Operating Status of Motor.
1-1,1-3,
A-
```
```
Changes Waiting time to re-sending Initial Reset Commands from 100
to 15 ms when FW in memory is not imperfect.
1-2,1-
A-1,A-
```
```
Changes character waiting timer from 100 ms to 5 sec.
```
```
A4 Oct. 8, 99
```
```
1-5,A-5 Changes monitoring time from 3 sec to 20 sec and adds *4.
```

##### I

I. Introduction
This specification shows the transmission specifications between the IC and magnetic card reader/writer
[ 3S4YR-MVF(DL) Series ] with RS232 and the HOST terminal.

II. Applicable Card Reader / Writer

```
Track 1 Track 2 Track 3
```
```
IC card
controller
Module name Option
```
```
A R/W R/W R/W *1 Y *2 3S4YR-MVFW1JD-
B R/W R/W R/W N *3 3S4YR-MVFW1D-052*
C R/W R/W R/W *1 Y 3S4YR-MVFR7D-051L
*1 R/W : Magnetic reading and writing function
*2 Y : Provided
*3 N : No provided
*4 In case of this module, this specification should be read except Track 1 read / write and ICC function.
```
III. Applicable CPU / FW
Type Version Notes
CPU HBU-NA053 E
FW in nonvolatile memory HBU-NA073 D


##### II

IV. Reference Standards

- ISO/IEC 7816-3:
    Identification cards - Integrated circuit(s) cards with contacts
    - Part 3 : Electronic signals and transmission protocols
- ISO/IEC 7816-3/Amd.1:
    Identification cards - Integrated circuit(s) cards with contacts
       - Part 3 : Electronic signals and transmission protocols
       Amendment 1 : Protocol type T=1,asynchronous half duplex block transmission protocol
- ISO/IEC 7816-3/Amd.2:
    Identification cards - Integrated circuit(s) cards with contacts
    - Part 3 : Electronic signals and transmission protocols
    Amendment 2 : Revision of protocol type selection
- ISO/IEC 7816-4:
    Identification cards - Integrated circuit(s) cards with contacts
    - Part 4 : Inter-industry commands for interchange
- ISO/IEC 7810: 1995-08-
    Identification cards - Physical characteristics
- ISO/IEC 7811-1: 1995-08-
    Identification cards - Recording technique
    Part 1:Embossing
- ISO/IEC 7811-2: 1995-08-
    Identification cards - Recording technique
    Part 2:Magnetic stripe
- ISO/IEC 7811-3: 1995-08-
    Identification cards - Recording technique
    Part 3:Location of embossed characters on ID-1 cards
- ISO/IEC 7811-4: 1995-08-
    Identification cards - Recording technique
    Part 4:Location of read-only magnetic tracks - Tracks 1 and 2.
- ISO/IEC 7811-5: 1995-08-
    Identification cards - Recording technique
    Part 5:Location of read-only magnetic tracks - Tracks 3
- ISO 2111: 1985-02-
    Data communication -Basic mode control procedures -
    Code independent information transfer
- EMV 3.0: June 30 ‘
    EMV ’96 Integrated Circuit Card Specification for Payment Systems
    Part I - Electromechanical Characteristics, Logical Interface, and Transmission Protocols
- Errata 1.0: Jan 31 ‘
    EMV ’96: ICC Specifications for Payment Systems
- EMV 3.1.1: May 31 ‘
    EMV ’96 Integrated Circuit Card Specification for Payment Systems
    Part I - Electromechanical Characteristics, Logical Interface, and Transmission Protocols


##### III

V. Notice for IC card (ICC)
OMRON standard ICC controller and FW (firm ware) can’t almost execute perfectly all customers ICC(s)
because ISO standard and also ICC(s) is modified frequently. OMRON should check your customer’s ICC if
you can get it and it’s specification.

VI. Character Code Expression Method
-XXH shows the HEX Code.
"X" shows the ASCII Code.

VII. Definition of Terminology

- HOST HOST Terminal
- C/R Card Reader
- Default Set value on the C/R side when power is turned ON.
- SS Magnetic Data Start Sentinel
- ES Magnetic Data End Sentinel
- LRC Magnetic Data Longitudinal Redundancy Check
- VRC Magnetic Data Vertical Parity
- ICC Integrated Circuit Card
- ATR Answer to Reset
- PTS Protocol type selection
- APDU Application Protocol Data Unit
- TCK Check Character
- IFS maximum information field size
- IFDS IFS for the interface device
- F Indicated values of the clock rate conversion factor
- D Indicated values of the bit rate adjustment factor
- DL Program Down Loading

```
S0: Front end sensor
S2: Mid-position sensor
S4: Rear-end sensor
SW1: Magnetic stripe detection head
SW2: Card width detection switch
SW3: Shutter echo sensor
SW4: ICC contact echo sensor
```

1 Transmission Specifications

```
1.1 Basic Transmission Specifications
```
```
Item Contents
Electronic Interface RS232 Interface
Synchronous Method Start-Stop Synchronization Method
Communication Method Half-duplex Method
Transmission Speed 1200, 2400, 4800, 9600, 19200 bps
Automatic Recognition *
Start Bit : 1 bit
Data: 8 bit
Vertical Parity Bit: 1 bit (even)
```
```
Character Format
```
```
Stop Bit : 1 bit
Character Code ASCII, Binary
Error Detector Horizontal Parity Check (BCC) : even
Vertical Parity Check : even
Bit Sending Sequence LSB Priority
*1 The HOST should sent one of “ Initial Reset “ command for transmission speed
setting between the HOST and the C/R right after power turns on or down loading
processing completed correctly. If the HOST has sent a data except “Initial Reset” command( ex.
DLE-EOT ), it should send “Initial Reset” command after 15 ms.
```
```
1.2 Transmission Control Method
```
- Command Response Method
- The C/R executes the designated processing corresponding to the command received from the HOST.
- The results are sent to the HOST as a response.

```
1.3 Transmission Control Codes
```
```
Code Value Meaning
DLE STX 10H 02H Characters showing the start of text for the Command or Response.
DLE ETX 10H 03H Characters showing the end of text for the Command or Response.
DLE ENQ 10H 05H Characters showing Command Execution Designation or Request
for Response Retransmission.
DLE ACK 10H 06H Positive Response Characters showing that the Command sent
from the HOST has been received normally.
DLE NAK 10H 15H Negative Response Characters showing the Command sent from
the HOST has been received abnormally.
DLE EOT 10H 04H Characters showing Transmission Interruption or Command
Execution Interruption.
DLE 10H Transparent Mode control code in text
```

```
1.4 Message Format
1) Command/Response Format
```
- Only one Command or Response is in the Text.
 - BCC is calculation result by an exclusive logic (XOR) from the Text beginning (after STX) to ETX.
- However, the following are excluded from BCC calculation.
DLE (10H) added by the Transparent Mode
DLE (10H) of the Transmission Control Code “ DLE ETX “
-The BCC Vertical Parity is regarded as the BCC Parity.
-The maximum transmission delay between each characters from the DLE to ETX, BCC of the HOST or
the C/R is within 5 sec.

2) Useable codes in the Text

```
*1 [Transparent Mode]
If "DLE(10H)" character is used in of the text as a part of command or response, double DLE(10H)
must be transmitted as below for transmission.
For details, see ISO 2111 “4. Presentation of data” and “5. Reception of data”.
```
```
DLE (10H) -> DLE DLE (10H 10H)
```
```
Text data Added DLE ( exclude BCC calculation )
```

```
1.5 Transmission Control Procedure
1.5.1 Transmission beginning
Automatic recognition of Transmission speed (baud rate ) between the C/R and the HOST is done by
one of the “ Initial Reset “ command from the HOST. Therefor , first of all, the HOST should send one of
the “ Initial Reset “ command after power turns on. If the HOST has sent the data except “Initial Reset”
command( ex. DLE-EOT ), it should send “Initial Reset” command after 15 ms.
```
```
1.5.2 Normal Operation Sequence
```
```
1.5.3 Recovery Operation Sequence
1) Monitoring time-out happens while the HOST is waiting for ACK from the C/R.
(The HOST re-sends the Command.)
```
```
*1: See 1.6Transmission Control Matrix.
```
```
2) When the HOST Receives NAK from the C/R. (Command is resent from the HOST)
```
```
*1: The C/R detects Receiving Error.
(Vertical Party, BCC and monitoring time-out happens Between Characters)
```
3) When the HOST detects an error during receiving of ACK from the C/R.
(The HOST re-sends the Command.)

```
*1: The HOST detects Receiving Error.
```
##### *


4) When monitoring time-out happens while the HOST is waiting for Response from the C/R.
(The HOST re-sends ENQ and requests a Response from the C/R.)

```
*1: See 1.6Transmission Control Matrix.
```
5) When the HOST detects an error during receiving of Response from the C/R.
( The HOST re-sends ENQ and requests resending of the response from the C/R. )

```
*1: The HOST detects Receiving Error.
```
```
1.5.4 Interruption of Transmission and Command to the C/R from the HOST.
By sending "DLE EOT" from the HOST, interruption of transmission or processing command can be
specified to the C/R. But interruption of transmission disables in down loading. For more detail, see
Annex. E.
```
1) Before the HOST Sends the Command (Interruption of Transmission from the HOST)

2) After the HOST Sent the Command (Command canceled from the HOST)

3) After the HOST sent ENQ ( Forced interruption of the processing command from the HOST )

```
4) While the C/R sends the Response (Transmission Interruption from the HOST)
```
##### *


1.6 Transmission Control Matrix
1) HOST Control (for reference)
Receiving Codes from C/R HOST Receiving Monitoring
DLE ACK DLE NAK DLE STX DLE ETX BCC Other Codes Time-out Monitoring Time
1 Waiting for
DLE ACK
after sent command

```
DLE ENQ
Sends
-> goes to
status 2
```
```
Re-sends
Command
-> remain in
status 1 *
```
```
Ignores Ignores Ignores Re-sends Command
-> remains in status 1
*
```
```
*
```
```
2 Waiting for
Response Receiving
after sent DLE ENQ
```
```
Ignores Ignores Clears Buffer
-> goes to
status 3
```
```
Ignores Ignores Re-sends DLE ENQ
-> remains in status 2
*
```
```
*
```
```
3 Waiting for DLE ETX
BCC in Response
receiving
```
```
Ignores Ignores Clears Buffer
```
```
-> remains in
status 3
```
```
Sends the next
command when
the receiving is normal
-> goes to status 1
Re-sends DLE ENQ
when receiving
is abnormal.
-> goes to status 2 *
```
```
Stores Data
```
```
-> remains in
status 3
```
```
Re-sends DLE ENQ
```
```
-> goes to status 2
*
```
```
20 seconds
*
```
```
*1 : Monitoring Time for waiting "DLE ACK" after the HOST had sent the command should be 5.02sec or
more.
When Sending/Receiving Switching-over Time of C/R is extended by the Initial Reset Command from
the HOST, the HOST should be monitored the time which is this value plus 5.02sec. (Refer to 4.1)
*2 : Monitoring Time of waiting Response of the HOST is different to each command. Usually 10 seconds or
more is recommended. For commands which is accompanied human operation (e.g., Insertion,
takeout ), this human operation time should be added to monitoring time of response, Also, when the
number of retries accompanying mechanical operation (moving) increases, one second per re-trying
should be added.
*3 : The number of re-transmission is decided by the HOST and should be decided more than one time.
The HOST should execute the Error Processing when the number of trying exceeded.
*4: A value of the monitoring time is different by the transmission speed and the response length. 20
seconds is the value of the monitoring time which the transmission speed is 1200 bps. The value of it is 3
seconds by 9600 bps.
```
```
2) C/R Control
Receiving Codes from HOST C/R Receiving Monitoring
DLE ENQ DLE STX DLE EOT DLE ETX BCC Other Codes Time-out Monitoring Time
1 Idle Re-sends
Response
-> remains status 1
```
```
Clears Buffer
-> goes to status 2
```
```
Execution
Interruption
->remains in
status 1
```
```
Ignores Ignores Ignores Ignores
```
```
2 Waiting for
DLE ETX
BCC in
Command
Receiving
```
```
Ignores Clears Buffer
-> remain in
Status 2
```
```
Execution
Interruption
-> goes to
status 1
```
```
When receiving is normal,
sends DLE ACK
-> goes to status 3
When receiving is
abnormal, sends DLE NAK
-> goes to status 1
```
```
Data Store
-> remains in
status 2
```
```
DLE NAK
Sends
-> goes to
status 1
```
```
5sec
(Between
characters)
```
```
3 Waiting for
DLE ENQ
after sent
DLE ACK
```
```
Sends response
after command
execution
-> goes to status 1
```
```
Clears Buffer
-> goes to status 2
```
```
Execution
Interruption
-> goes to
status 1
```
```
Ignores Ignores Ignores Ignores
```
```
While the C/R is processing a command except DL processing, all characters except “ DLE EOT“ from
HOST are ignored. Also, see Annex E about “DLE EOT” in DL processing.
```

2 Time Chart of Transmission Control Signal Line
The signal name is shown on the C/R side.

```
2.1 DTR Signal
```
```
*1:HOST should be transmitted data after DTR Signal turns ON.
DTR Signal break continues the interval of max. 300ms after DL completion response is sent. After
confirmed the DTR Signal rise, HOST should send an initial reset command.
```
```
2.2 Transmission Interruption by the CTS Signal
The figure below shows CTS Signal from the HOST turns OFF during Response Transmission by the
C/R.
```
```
(1) When the CTS Signal from the HOST is turned OFF during Response Transmission from the C/R,
the C/R interrupts the transmission after maximum characters of two was sent.
(2) The C/R reopens the transmission within maximum delay of 1ms after turning ON the CTS Signal
from the HOST.
```
```
*
```

3 Message Specifications
Explanation of each column in the tables below.

- Column of Length shows the number of byte(s) for each item.
- Column of Data shows the contents of each item.

```
3.1 Command Format (HOST -> C/R)
A Command is the text which indicates execution processing to the C/R from the HOST.
```
```
IDN CMD Command Parameter
Length 1 2 Variable Length (0-2054 bytes)
Data “C” See 3.3 For details , see 4
```
```
IDN: Indicates code of the command. The code is “C” (43H).
CMD: Indicates the command. (See 3.3)
Command Parameter: This is defined as the details of CMD processing. However, there is also CMD
without Command Parameter.
```
```
3.2 Response Format (C/R -> HOST)
A Response is the text which is transmitted from the C/R to the HOST. It is as the processing results for
the command text which was sent from the HOST to the C/R.
(1) JDG
```
- The HOST should judge the processing results by the JDG Code in the Response Message.
- “P” (50H) indicates a positive response which the processing had been completed normally.
- “N” (4EH) indicates a negative response which the processing had been completed abnormally.
(2) RCM
RCM in the Response Message is the same code as the command (CMD) which had been defined
processing.

```
3.2.1 Positive Response Format
```
```
JDG RCM RES Response data
Length 1 2 2 Variable Length ( 0-320 bytes)
Data “P” See 3.3 See 3.4.1 For details , see 5
```
```
(1) RES
```
- RES in the Response Message usually indicates the position data of the card in the C/R. (See
    3.4.1 )
- For the ICC Control Commands, the ICC Control Status is also indicated. (See 3.4.1 )
- For the DL relation commands, DL status is also indicated. (See 3.4.1 )
(2) Response Data
- Response data is indicated the data due to the processed commands from the HOST. (See 3.3)
- However, there are also no response data due to the command.

```
3.2.2 Negative Response Format
```
```
JDG RCM RES Response data
Length 1 2 2 Variable Length (0-62 bytes)
Data “N” See 3.3 See 3.4.2 For details , see 3.
```
```
(1) RES
RES in the Response Message indicates the Error Code due to the processed commands from the
HOST (See 3.4.2 )
(2) Response data
```
- Response data is only added as a response when an error occurred and the command is defined
    which is requested Error Track Number(s) or ATR. (See 3.3)
- Response data is only added as a response when a command is defined which is requested
    response data when DL processing is executing or new FW loading hasn’t yet completed in DL
    processing. ( See 3.3 Annex E )


```
3.3 Table of Commands
Definition of Terminology
Track A : Multi-track Numbers
Track B : Single-track Number
Mag. Data A : Write Magnetic Data
Mag. Data B : Single-Track Number + Write Magnetic Data
Mag. Data C : Multi-track Number + Write Magnetic Data
Mag. Data D : Read Magnetic Data
Mag. Data E : Multi-track Number + Read Magnetic Data
Mag. Data F : Reads Magnetic Data (Multi-track / All tracks )
```
```
3.3.1 Card Reader Control Commands (RCC)
(1) Table of Basic Commands(1/3)
Command
Name
```
```
CMD
(ASCII) Function
```
```
Command
Parameters Ref.
```
```
Response
Data Ref.
“00” Initializes the C/R then returns card to takeout position if card
is in the C/R.
```
```
Initial Set
Data
```
```
4.1 None -
```
```
“01” Initializes the C/R then ejects card through to rear-end if card
is in the C/R.
```
```
Initial Set
Data
```
```
4.1 None -
```
```
“02” Initializes the C/R then holds card in standby position if card is
in the C/R.
```
```
Initial Set
Data
```
```
4.1 None -
```
```
“04” Initializes the C/R then returns card to takeout position if card
is in the C/R (No shutter control when no card is in).
```
```
Initial Set
Data
```
```
4.1 None -
```
```
“05” Initializes the C/R then ejects card through to rear-end if card
is in the C/R (No shutter control).
```
```
Initial Set
Data
```
```
4.1 None -
```
```
Initial Reset
*
```
```
“06” Initializes the C/R then holds card in standby position if card is
in the C/R (No shutter control).
```
```
Initial Set
Data
```
```
4.1 None -
```
```
Status Sense “10” Reads the C/R condition. None - None -
“11” Reads sensors status. *2 None - Sensor info. 5.
“:0” Permits insertion from front and waits infinitely card (w/o mag.
Stripe) insertion. Takes in card then transports to rear standby
position. *
```
```
None - None -
```
```
“:1” Denies card insertion after interrupted card insertion state by
“:0”, “:2” or “:3”.
```
```
None - None -
```
```
“:2” Permits insertion with mag. Stripe card from front and waits
infinitely card insertion. Takes in card then transports to rear
standby position. *
```
```
None - None -
```
```
Insertion
Permission
/Denial
```
```
“:3” Permits insertion from rear waits infinitely card (w/o mag.
stripe) insertion. Takes in card then transports to front standby
position. *3 *
```
```
None - None -
```
```
“20” Permits insertion w/o mag. stripe from front and waits. Takes
in card then transports to rear standby position.
```
```
None - None -
```
```
“21” Permits insertion with mag. stripe from front and waits. Takes
in card then transports to rear standby position.
```
```
None - None -
```
```
“22” Permits insertion w/o mag. stripe from rear and waits. Takes in
card then transports to front standby position. *
```
```
None - None -
```
```
“23” Permits insertion w/o mag. stripe from front and waits. Takes
in card, then return to take out position temporary and take in
card immediately and transports to rear standby position.
```
```
None - None -
```
```
Intake *3 *
```
```
“24” Permits insertion with mag. stripe from front and waits. Takes
in card, then return to take out position temporary and take in
card immediately, and transports to rear standby position.
```
```
None - None -
```
*1: First of all, the HOST has to send one of these “Initial Reset” command for automatic recognition of
transmission speed and setting of transmission format (see 1.4 and annex A) between the HOST to the
C/R. These setting is only valid by one of initial reset command sending from the HOST after power turned
on.
And also these command is used confirmation of movement of shutter, solenoids and motor.
After that, card is returned, ejected or held if card exists inside.
*2: The HOST can get the sensor information, e.g. output status of position sensor after card was took in.
*3: All tracks read data is implicitly stored in memory after in-take. Then Read data is transmitted after
processed it by a Read command.
*4 Monitoring time for Card insertion is specified by “W0”.
*5: The HOST should send the command after it confirms the card have been taken out.


(1) Table of Basic Commands (2/3)

```
Command
Name
```
```
CMD
(ASCII)
Function Command
Parameters
Ref.
```
```
Respons
e
Data
```
```
Ref.
```
```
“30” Transports card to Takeout position of front. None - None -
“31” Ejects card through to rear end. None - None -
```
```
Return
```
```
“32” Transports the MM-sensor card to read start position. None - None -
Waiting for
Removal *
```
```
“90” Waits for card to be taken out from front taken-out
position while is specified the monitoring time by “W1”.
```
```
None - None -
```
```
“40” Re-intakes card to rear standby position from front
takeout position.
```
```
None - None -
```
```
“41” Re-intakes card from front takeout position and ejects to
Rear.
```
```
None - None -
```
```
Re-intake *
```
```
“42” Re-intakes card to rear standby position from front
takeout position. And sends read data of a lowest track
number that was able to read correctly during intake.
```
```
Track A 4.2 Mag. Data E 5.
```
```
“60” No read operation (only transportation). None - None -
“61” Reads ISO #1 and sends data. *2 None - Mag. Data D 5.
“62” Reads ISO #2 and sends data. *2 None - Mag. Data D 5.
“63” Reads ISO #3 and sends data. *2 None - Mag. Data D 5.
“68” Reads multiple magnetic tracks and sends the read
data of the lowest track number which was read
correctly. *2 *3 *
```
```
Track A 4.2 Mag. Data E 5.
```
```
“69” Sends the read data in memory by this command. *4 Track B 4.3 Mag. Data D 5.
```
```
Read
```
```
“6A” Sends multi-tracks data in the memory by this command
and parameter. *2 *
```
```
Track A 4.2 Mag. Data F 5.
```
```
“71” Writes magnetic data onto ISO #1 track. Mag. Data A 4.4 None -
“72” Writes magnetic data onto ISO #2 track. Mag. Data A 4.4 None -
“73” Writes magnetic data onto ISO #3 track. Mag. Data A 4.4 None -
“78” Sets write data in memory track by track for Multiple
Magnetic tracks (No Write processing).
```
```
Mag. Data B 4.5 None -
```
```
Write
```
“79” Writes data of Multiple-Magnetic tracks at one time. Mag. Data C 4.6 Error track *5 5.
*1: Monitoring time is specified by “W2”.
*2: In case that read data was memorized in C/R, the HOST can get immediately the read data without card
transporting. The other hand, in case of no memory of read data , C/R executes re-read according to the
setting retry number. In case that the retry number was set zero or error is continuing after retry was done,
the error response is sent.
*3: The HOST can get only single track data even if multi-track is read by “68” command. Therefore the HOST
should use together with “69” or “6A” command in case of the other track(s) data reading.
For detail of response, see 5.3.
*4: Multi-read data in memory is transmitted at one time by related command.
*5: Error Track Number is transmitted to the HOST only when an error occurs.
*6: RES of positive response is transmitted the “card position” when the response was prepared.


(1) Table of Basic Commands (3/3)
Command
Name

```
CMD
(ASCII) Function
```
```
Command
Parameters Ref.
```
```
Response
Data Ref.
“Q0” Reads the number of ejected ( captured ) card(s) to
rear.
```
```
Number of None - Captured No. 5.
Cards
Captured “Q1” Initialized number of ejected ( captured ) card(s) to
rear (“000”). (*1)
```
```
None - None -
```
```
Cleaning “I0” Cleans head and or sensors with a Cleaning card
( back and forth motion is done 3rd. times.)
```
```
None - None -
```
```
Sensor Level
Read
```
```
“L0” Reads voltage of the C/R sensors. None - Level Info. 5.
```
```
“R0” Sets the retry number when read error occurred. Retry No. 4.7 None -
“R1” Sets the retry number when write error occurred. Retry No. 4.7 None -
```
```
Retry Number
Setting
“R3” Sets the retry number when return error occurred. Retry No. 4.8 None -
“W0” Sets the monitoring time till card is inserted
( Relating “20”,”21” and “22” ).
```
```
Monitor Time 4.9 None -
```
```
“W1” Sets the monitoring time till card returned to Front is
removed (Relating “90”).
```
```
Monitor Time 4.9 None -
```
```
Monitor Time
Setting
```
```
“W2” Sets the monitoring time till card is re-in-taken to
Rear ( Relating “40”,”41” and “42”).
```
```
Monitor Time 4.9 None -
```
```
“N0” Reads information of options installed. None - Option Info. 5.
“N1” Sets existence of P/F condenser. *1 P/F Condenser
Existence
```
```
4.10 None -
```
```
“N2” Sets one of magnetic head type within “No Head”,
“Read-only”, and “Read/Write”. *
```
```
Mag. Head Type 4.11 None -
```
```
“N3” Sets using of I/O port. *1 I/O Port using 4.12 None -
```
```
Option Device
Read/ Setting
```
```
“NA” Erases Version Information in memory and the data
of Option Information is changed to “No setting”. *
```
```
None - None -
```
```
Version Read “V0” Reads FW version. None - Version Info. 5.
“V1” Reads FW version of ICC control part. None - Nonvolatile Memory
FW Version Info.
```
```
5.
```
```
“P0” Sets deactivation of output port(s). Output Port 4.25 None -
“P1” Sets activation of output port(s). Output Port 4.25 None -
“P2” Sets deactivation of designated output port(s) during
the specified time.
```
```
Output Port 4.25 None -
```
```
“P3” Sets activation of designated output port(s) during
the specified time.
```
```
Output Port 4.25 None -
```
```
“P4” Repeats activation and deactivation of designated
output port(s) according to the specified time.
```
```
Output Port 4.25 None -
```
```
I/O Port *
```
```
“P5” Reads status of input port(s). None - Input Port 5.
“T0” Deactivation time of output port(s) is set (Relating
“P2”).
```
```
Output Port
Setting Time
```
```
4.27 None -
```
```
“T1” Activation time of output port(s) is set (Relating “P3”). Output Port
Setting Time
```
```
4.27 None -
```
```
“T2” Deactivation time of output port(s) is set when
activation and deactivation is repeated (Relating
“P4”).
```
```
Output Port
Setting Time
```
```
4.27 None -
```
```
I/O Port Time
Setting
```
```
“T3” Activation time of output port(s) is set when
activation and deactivation is repeated (Relating
“P4”).
```
```
Output Port
Setting Time
```
```
4.27 None -
```
```
“Y0” Reads control information of ICC. None - ICC Control Info. 5.
“Y1” Sets the reference standard used in commands
related to ICC. *
```
```
ICC Reference
Standard
```
```
4.28 None -
```
```
“Y2” Sets the monitoring time for waiting for reception
used in commands related to ICC. *
```
```
Timer Value for
Waiting for
Reception
```
```
4.29 None -
```
```
“Y3” Sets IFSD control method used in commands related
to ICC. *
```
```
IFSD Control
Method
```
```
4.30 None -
```
```
ICC Control
Information
```
```
“Y4” Sets TCK control method used in commands related
to ICC. *
```
```
TCK Control
Method
```
```
4.31 None -
```
*1 These commands can’t execute under “Insertion permission” ( until the card is taken in after “Insertion
permission” command was sent. ) In that case, C/R sends the response of sequence error (“Nxx01”).
*2 All I/O ports is de-active state after power turns on.


(2) Table of Extended Commands
Command
Name

```
CMD
(ASCII) Function
```
```
Command
Parameters Ref.
```
```
Response
Data Ref
“6B” Intakes w/o stripe card from front + Reads *3 Track A 4.2 Mag. Data E 5.
“6C” Intakes w/o stripe card from front + Reads
+ Returns to Front *
```
```
Track A 4.2 Mag. Data E 5.
```
```
“6D” Intakes w/o stripe card from front + Reads
+ Ejects to Rear end *
```
```
Track A 4.2 Mag. Data E 5.
```
```
“6E” Intakes with Mag. Stripe card from front + Reads
*
```
```
Track A 4.2 Mag. Data E 5.
```
```
“6F” Intakes with Mag. Stripe card from front + Reads
+ Front Return *
```
```
Track A 4.2 Mag. Data E 5.
```
```
“6G” Intakes with Mag. Stripe card from front + Reads
+ Ejects to Rear end *
```
```
Track A 4.2 Mag. Data E 5.
```
```
“6H” Intakes from Rear + Reads *3 *4 Track A 4.2 Mag. Data E 5.
“6I” Intakes from Rear + Reads + Returns to Front
*3 *
```
```
Track A 4.2 Mag. Data E 5.
```
```
“6K” Reads + Returns to Front Track A 4.2 Mag. Data E 5.
```
```
Read
```
```
“6L” Reads + Ejects to Rear end Track A 4.2 Mag. Data E 5.
“7B” Intakes w/o stripe card from front + Writes *3 Mag. Data C 4.6 Err. Track No.*1 5.
“7C” Intakes w/o stripe card from front + Writes
+ Returns to Front *
```
```
Mag. Data C 4.6 Err. Track No.*1 5.
```
```
“7D” Intakes w/o stripe card from front + Writes
+ Ejects to Front *
```
```
Mag. Data C 4.6 Err. Track No.*1 5.
```
```
“7E” Intakes with Mag. Stripe card from front + Writes
*
```
```
Mag. Data C 4.6 Err. Track No.*1 5.
```
```
“7F” Intakes with Mag. Stripe card from front + Writes
+ Returns to Front *
```
```
Mag. Data C 4.6 Err. Track No.*1 5.
```
```
“7G” Intakes with Mag. Stripe card from front + Writes
+ Ejects to Front *
```
```
Mag. Data C 4.6 Err. Track No.*1 5.
```
```
“7H” Intakes from Rear + Writes *3 *4 Mag. Data C 4.6 Err. Track No.*1 5.
“7I” Intakes from Rear + Writes + Returns to Front
*3 *
```
```
Mag. Data C 4.6 Err. Track No.*1 5.
```
```
“7K” Writes + Returns to Front Mag. Data C 4.6 Err. Track No.*1 5.
```
```
Write
```
```
“7L” Writes + Ejects to Rear end Mag. Data C 4.6 Err. Track No.*1 5.
“D0” Designates Front Return when Read is Normal Execution Desig. Data 4.13 None -
“D1” Designates Front Return when Read is Error Execution Desig. Data 4.13 None -
“D2” Designates Front Return when Write is Normal Execution Desig. Data 4.13 None -
“D3” Designates Front Return when Write is Error Execution Desig. Data 4.13 None -
“D4” Designates Rear Eject when Read is Normal Execution Desig. Data 4.13 None -
“D5” Designates Rear Eject when Read is Error Execution Desig. Data 4.13 None -
“D6” Designates Rear Eject when Write is Normal Execution Desig. Data 4.13 None -
```
```
Return
Conditions
Parameters *
```
```
“D7” Designates Rear Eject when Write is Error Execution Desig. Data 4.13 None -
“S0” Sets Transmission Format Change of Magnetic
Data
```
```
Transmission Format 4.14 None -
```
```
“S1” Sets Format Change of Magnetic Data Mag. Format 4.15 None -
```
```
Magnetic
Format
Change
Setting “S2” Sets Start Position Change of Write for Start
Sentinel (SS)
```
```
Position Data 4.16 None -
```
*1 Error Track Number is transmitted only when an error occurred.
*2 The return condition parameters are only effective when the extended commands, read or write ,was used.
*3 Monitoring time for Card insertion is specified by “W0”.
*4 The HOST should send the command after it confirms the card have been taken out.


```
3.3.2 ICC Control Commands (ICC)
(1) Table of Basic Commands
Command
Name
```
```
CMD
(ASCII) Function
```
```
Command
Parameters Ref.
```
```
Response
Data Ref.
ICC Press “C0” Transports to ICC access position and presses ICC
contact.
```
```
None - None -
```
```
ICC Release “C1” Releases ICC contact from ICC. None - None -
ICC Activation “C2” Activates ( Cold Reset ) ICC and sends ATR.
It is impossible to designate the automatic execution of
PTS by the C/R.
```
```
Node address 4.17 ATR Info. *1 5.
```
```
ICC
Deactivation
```
```
“C3” Deactivates ICC. None - None -
```
```
ICC Control
Information *
```
```
“C4” Sets the monitoring time for waiting for reception used
in commands related to ICC.
```
```
ICC Control
Setting
```
```
4.32 None -
```
```
ICC Cold
Reset
```
```
“E0” Activates to ICC. It is possible to set the execution of
PTS independently.
```
```
ATR/NAD
setting
```
```
4.18 ATR/PTS
Inf. *
```
```
5.
```
```
ICC Warm
Reset
```
```
“E1” Executes warm reset to ICC. It is possible to set the
execution of PTS independently.
```
```
ATR/NAD
setting
```
```
4.18 ATR/PTS
Inf. *
```
```
5.
```
*1 ATR information (“C2”,”E0” and “E1”) is transmitted to the HOST only when the ATR information from the
ICC was read correctly. For IC Commands usage, see Annex C and D.
*2 This command can be used to make compatible with the present version.
If ICC control information setting command (“C4”) was used, please change the command code from “C4”
to “Y1”.

```
(2) Table of Extended Commands
Command Name
CMD
(ASCII) Function
```
```
Command
Parameters Ref.
```
```
Response
Data Ref.
ICC Multiple “C5” ICC Press (“C0”)+ ICC Activation (“C2”) NAD setting 4.17 ATR Info. *1 5.
processing “C6” ICC Deactivation (“C3”)+ ICC Release (“C1”) None - None -
ICC Cold Reset “G1” Press ICC + ICC Cold Reset (“C0”+”E0”) ATRNAD
setting
```
```
4.18 ATR/PTS
Inf. *
```
```
5.
```
*1 ATR information (“C5” and “G1”) is transmitted to the HOST only when the ATR information from the ICC
was read correctly. For ICC Commands usage, see Annex C and D.


```
(3) IC Card Direct Control Commands (IDC)
Command
Name
```
```
CMD
(ASCII) Function
```
```
Command
Parameters Ref.
```
```
Response
Data Ref.
T=
Transmission
```
```
“F0” Sends or receives data between the HOST and the ICC
using Protocol Type T=0.
```
```
T=0 Sending
Data
```
```
4.19 T=0 Receiving
Data
```
```
5.
```
```
T=
Transmission
```
```
“F1” Sends or receives data between the HOST and the ICC
using Protocol Type T=1. This command should be used
for sending/receiving of data unchained or for
transmitting the last part of data chained.
```
```
T=1 Sending
Data
```
```
4.20 T=1 Receiving
Data
```
```
5.
```
```
T=1 Continuous
Transmission
```
```
“F2” Sends data chained of Protocol Type T=1. This
command should be used to send after divided the data
when the data length to be send is longer than the
command parameter. “F1” should be used in case that
sending data length of the last block is within command
parameter.
```
```
T=1 Sending
Data
```
```
4.20 T=1 Receiving
Data
```
```
5.
```
```
T=1 Continuous
Receiving
```
```
“F3” Receives data chained of Protocol Type T=1. This
command should be used for continuous receiving of
data when response status from the C/R is “21”.
```
```
None - T=1 Receiving
Data
```
```
5.
```
```
T=1 interruption
Completion
```
```
“F4” Continuous sending/receiving of Protocol Type T=1 is
forcedly terminated.
```
```
None - None -
```
```
T=1 Extended
Transmission
```
```
“F6” Sends or receives data between the HOST and the ICC
using Protocol type T=1. This command should be used
for sending/ receiving of unchained or chained data
which is the last block. The command APDU is copied
onto the information field of an I-block without any
change.
```
```
T=1 Extended
Sending Date
```
```
4.21 T=1 Receiving
Data
```
```
5.
```
```
T=1 Extended
Continuous
Transmission
```
```
“F7” Sends data chained of Protocol Type T=1. This
command should be used to send after divided the data
when the data to be sent is longer than the command
parameter. “F6” should be used in case that sending
data length of the last block is within command
parameter. The Command APDU is copied onto the
information field of an I-block without any change
```
```
T=1 Extended
Sending Date
```
```
4.21 T=1 Receiving
Data
```
```
5.
```
```
PTS Request “F8” Sends or receives PTS request between the HOST and
the ICC.
```
```
Protocol Type 4.22 PTS
information
```
```
5.
```
Note: For ICC Commands usage, see Annex C and D.

```
3.3.3 Table of Command related Down Load (DLC)
Command Name (ASCII)CMD Function ParametersCommand Ref. ResponseData Ref.
DL Start “d0” Designates DL start. No. of DL Block 4.23 None -
DL Transmission “d1” Sends DL Data ( FW ). DL Data 4.24 None -
DL Completion “d2” Sends DL completion. None - Ver. Info. in Memory 5.
Memory Check “c0” Checks SUM and reads FW version in
memory.
```
```
None - Ver. Info. in Memory 5.
```
USER Info. Read “u0” Reads the user information in memory. USER info. length 4.26 USER Info. Data 5.
Note: For DLC commands usage, see Annex E.


3.4 Table of Responses
3.4.1 Status Table of Positive Response
Response status (RES) of Positive Response Format shows the table below.

```
RES
(ASCII) Meaning
“ 00 ” No card is in the C/R.
“ 01 ” A card is in the Takeout Position.
“ 02 ” A card is in the C/R.
“ 04 ” A card is in Read Start Position of the MM Sensor
“ 10 ” IC Contact is pressed to the ICC.
“ 11 ” ICC is in the Activation Status.
“ 20 ” Transmission to the ICC is completed. (with/ without Receiving Data, with SW1 + SW2)
“ 21 ” Continuous receiving Status from the ICC. (with Receiving Data, without SW1 + SW2)
“ 22 ” Continuous sending Status to the ICC. (without Receiving Data, without SW1 + SW2)
“ 23 ” Ends the Completion of ICC Transmission by forcedly interruption.
“ 30 ” In Down loading.
“ 31 ” Normal Completion of Down loading, Status of Initial Reset Waiting.
```
3.4.2 Status Table of Negative Response (Error Code)
Response status (RES) of Negative Response Format shows the table below.

```
(1) Error code table (1/8)
RES
(ASCII) Sorts of Error Meaning
“00” Undefined Command
Receipt
```
```
-- - The HOST used a unwritten Command in specification.
```
```
“01” Command Sequence
Error
```
```
-- - The HOST sent a disable command in the present state.
```
```
“02” Command Data Error -- - The HOST sent a wrong data of command parameter.
“03” Write Track setting Error -- - The HOST designated write for track(s) without write data.
Note: Host should be checked the content of command and sequence.
```

(2) Error code table (2/8)
RES
(ASCII) Sorts of Error Meaning
“10” Card Jam C/R abnormality
*1

- The C/R couldn’t carry the card in the C/R to the correct
    position.
- The C/R couldn’t return the card to the take out position due
    to the shutting of insertion mouth.
- The C/R couldn’t carry the card in-taken from front to the
    correct position.
“11” Shutter Abnormality C/R abnormality
*1
- The C/R couldn’t open the shutter.
- The C/R couldn’t detect the shutter opening due to the trouble
of shutter echo sensor.
- All condition was to be closed the shutter , but the C/R
couldn’t close it.
- The shutter is forcibly closed when shutter is opening by “32”
(MM card return) or “23”,”24”(intake). Or the C/R couldn’t
detect closing condition of shutter due to the trouble of
shutter echo sensor.
“12” Sensor Abnormality C/R abnormality
*1
- Sensor S0 and S4 is shaded when taken in the card was
carried.
“13” Motor Abnormality C/R abnormality
*1
- The C/R rotated motor, but the C/R couldn’t detect pulse of
210 bpi encoder to be connected the motor due to the
encoder trouble.
- The C/R rotated motor , but Motor didn’t rotate.
“14” Card Drawn Out C/R abnormality
*1
- All sensor (S0, S2 and S4) was lighted after card had in-
taken.
- The card may be drawn out while waiting to be processed.
“15” Card Jam
in Re-intake

```
C/R abnormality
*1
```
- The C/R couldn’t carry the card from the front to the standby
    position by “40” and “41” (re-intake).
- The C/R couldn’t carry the card from the front to the standby
    position by “23” and “24” (intake).
“16” Card Jam at
the Rear-end

```
C/R abnormality
*1
```
- S4 sensor at the rear is shading after card had ejected.

```
“17” 75 bpi encoder
abnormality
```
```
C/R abnormality
*1
```
- The C/R rotated motor and 210bpi pulse was normality, but
    the C/R couldn’t detect pulse of 75 bpi encoder to be
    connected the motor due to the encoder trouble.
“18” Power Down
Detection
*2
*3
*4

```
C/R abnormality
*1
```
- Power Down is detected during command processing or
    before processing (include initial reset command).

```
“19” Waiting Initial Reset
*3
*4
```
```
Waits initial
reset
*1
```
- The C/R received a command exclude Initial Reset command
    after power turned on.
- The C/R received a command exclude Initial Reset command
    after the C/R sent the response of Power Down
    Detection(“19”).
Note:
*1: The C/R waits “initial reset “( “00”, “01”, “02”, “04” ,”05” and “06”) command when the HOST received the
error code.
*2: When a command is executing exclude initial reset, the response is sent in case that power is restored
in short time and transmission speed etc. in memory of CPU was memorized.
*3: For more detail , see Annex G.
*4: The Host sends “initial reset“ (“00”, “01”, “02”, “04” ,”05” and “06”) command after waiting for 15ms from
error response reception.


(3) Error code table (3/8)
RES
(ASCII) Sorts of Error Meaning
“20” Too Long Card Card abnormality
*1

- Longer card is inserted from front and the C/R detect state
    that card width switch is ON , sensor S0 and S2 is shared.
- Longer card is inserted from rear and the C/R detect state
    that sensor S0, S2 and S4 is shared.
“21” Too Short Card Card abnormality
*1
- Shorter or with hole(s) card is inserted from front and the C/R
detect state that sensor S0 and S2 is lighted.
- Shorter or with hole(s) card is inserted from rear and the C/R
detect state that sensor S2 and S4 is lighted.
Notes:
*1: The C/R waits “return”(“30”) and “initial reset “( “00” and “04” ) command after the HOST received the
error code.

(4) Error code table (4/8)
RES
(ASCII) Sorts of Error Meaning
“32” Card Position Change Warning
*1

- Card position which is taken in moves.

```
“33” Memory Information
Abnormality
```
```
Warning
*1
*2
```
- The SUM value of in memory. (the number of captured card,
    magnetic head type and existence of P/F condenser ) is
    incorrect. So the information will be destroyed.
- Host couldn’t set Option Information by “N1”, “N2”, or “N3”.
Notes:
*1: The HOST can sent a next command after the HOST received the error code.
*2: In case of this error, HOST should erase Option Information by “NA” command and set all Option
Information again by “N1”, “N2”, or “N3”.


(5) Error code table (5/8)
RES
(ASCII) Sorts of Error Meaning
“40” Read Error
( SS error )

```
Card abnormality
*1
```
- The C/R couldn’t detect SS-code in read data.

```
“41” Read Error
( ES error )
```
```
Card abnormality
*1
```
- The C/R couldn’t detect ES-code after SS-code in read data.

```
“42” Read Error
( VRC error )
```
```
Card abnormality
*1
```
- The C/R detects that SS code and VRC of next character is
    correct in read data. But VRC of following characters is
    detected Vertical parity error ( VRC error ).
“43” Read Error
( LRC error )

```
Card abnormality
*1
```
- The C/R detects that the character after ES in read data
    doesn’t coincide with result of LRC calculation.
“44” Read Error
( No Encode )

```
Card abnormality
*1
```
- Total bits to be read magnetic data is less than 20.
- No of bits to be read of ISO #1 is less than 10.
- No of bits to be read of ISO #2 or #3 is less than 8.
“45” Read Error
( No Data )

```
Card abnormality
*1
```
- The C/R detects that the character after ES is SS and then the
    next character coincide with result of LRC calculation in read
    data. (No data besides SS-ES-LRC)
“46” Read Error
(Jitter Error)

```
Card abnormality
*1
```
- This error doesn’t become above read error ( “40”-”45” ) but
    there are more than 10bits which is over permission value of
    Jitter in read data.
“49” Read Track setting
Error
-- - Specified track isn’t read.
“50” Write Error
( SS error )

```
Card abnormality
*1
```
- The C/R couldn’t detect SS code in verification after write.

```
“51” Write Error
( ES error )
```
```
Card abnormality
*1
```
- The C/R couldn’t detect ES code after SS code in verification
    after write.
“52” Write Error
( VRC error )

```
Card abnormality
*1
```
- The C/R detects that SS code and VRC of next character is
    correct in verification. But VRC of following characters is
    detected Vertical parity error ( VRC error ).
“53” Write Error
( LRC error )

```
Card abnormality
*1
```
- The C/R detects that the character after ES in verification
    doesn’t coincide with result of LRC calculation.
“54” Write Error
( No Encode )

```
Card abnormality
*1
```
- Total bits to be read is less than 20 in verification.
- No of bits to be read of ISO #1 is less than 10.
- No of bits to be read of ISO #2 or #3 is less than 8.
“55” Write Error
(Data discordance)

```
Card abnormality
*1
```
- The C/R detects that SS, ES VRC and LRC is correct. But the
    write data doesn’t coincide with read data.
“56” Write Error
( Jitter error )

```
Card abnormality
*1
```
- This error doesn’t become above write error ( “50”-”55” ) but
    there are more than 10bits which is over permission value of
    Jitter in read data.
Notes:
*1: Abnormality of magnetic data is detected. The HOST can sent next command continuously after the
HOST received the error code.

(6) Error code table (6/8)
RES
(ASCII)
Sorts of Error Meaning
“60” Card Taken Out
When Re-intake

```
Warning
*1
```
- The HOST sends Re-intake command ( “40”, “41” and “42” )
    when no card is in mouth of insertion.
- The card is taken out from mouth of insertion when the card is
    in mouth of insertion and Re-intake command is sent.
- The card is taken out or held from / in mouth of insertion when
    the card returned and re-intake by intake command (“23”,”24”)
“61” Insertion monitoring
Time is up

```
Warning
*1
```
- No card in-takes by intake command during Insertion
    monitoring Time.
“62” Take-out monitoring
Time is up

```
Warning
*1
```
- A card isn’t took out from the takeout position during take-out
    monitoring Time.
“63” Re-intake monitoring
Time is up

```
Warning
*1
```
- Card isn’t re-took in by Re-intake command during Re-intake
    monitoring Time.
“64” Card was held at
takeout position
during initial reset

```
Warning
*1
```
- When the card was in mouth of insertion the HOST sent initial
    reset command (ejects rear or keeps inside ). But the card isn’t
    took in ( e.g. hold by hand )
Notes:
*1: The HOST can sends next command continuously after the HOST received the error code.


(7) Error code table (7/8)
RES
(ASCII) Sorts of Error Meaning
“70” FW Imperfection Waits for DL
*1

- The C/R detects SUM value error in memory after power turned
    on.
- The C/R receives a command in DL exclude “d0” , “d1” and
    “ d2”.
- FW imperfection is detected in memory after power turns on.
“71” Initial CMD waiting
after FW loading
completion
*2

```
Waits for initial
reset
*3
```
- The HOST sends a command exclude initial reset command
    after the HOST received “31”( response of normal DL
    completion ).

Notes:
*1: The HOST should send “d0”,”d1” and “d2” according to DL sequence and should execute FW down
loading.
*2:The Host sends “initial reset“ (“00”, “01”, “02”, “04” ,”05” and “06”) command after waiting for 15ms from
error response reception.
*3: The C/R waits “initial reset “( “00”, “01”, “02”, “04” ,”05” and “06”) command after the HOST received the
error code.

(8) Error code table (8/8)
RES
(ASCII) Sorts of Error Meaning
“80” Receiving from ICC is
Impossibility

```
ICC abnormality
*1
```
- The C/R detects that receiving data from the ICC is over buffer
    size of the C/R in execution of T=0,T=1 protocol and PTS.
- The C/R can’t complete sending and receiving in execution of
    T=0,T=1 protocol and PTS when monitoring time was up.
- The C/R aborted ICC process ( ICC reference standard is
    “EMV3.0 Errata 1.0”.)
“81” ICC Solenoid
Abnormality

```
C/R abnormality
*2
```
- Impossible to press the contact.
- impossible to release the contact.
- Echo sensor of contact unit under pressing is detected OFF.
- Echo sensor of contact unit under releasing is detected ON.
“82” ICC Activation
Abnormality

```
ICC abnormality
*1
```
- The C/R detects short circuit when Vcc is supplied in activation
    processing.
- The C/R detects that monitoring time was up or parity error
    occurred in processing.
“84” ICC Communication
Abnormality

```
ICC abnormality
*3
```
- Monitoring time was up or parity error occurred in T=0 and
    T=1protocal execution, and the C/R can’t recovers after retry
    execution.
“85” ICC Compulsory
Abort Reception

```
ICC abnormality
*3
```
- The C/R receives forced Interruption ( S block: abort request )
    in T=0 and T=1protocal execution.
“86” ICC Reception Data
Abnormality

```
ICC abnormality
*3
```
- The C/R receives invalid block or data in T=0 and T=1protocal
    execution.
“87” Unsupported ICC ICC abnormality
*4
- The C/R receives unsupported ATR.

```
“88” ICC movement in
press
```
```
C/R abnormality
*2
```
- Sensor changes different status from S0&S2 was lighted and
    S4 was shared.
Notes:
*1: C/R deactivates automatically. HOST should releases contact and tries again to activate after press
contact after HOST received the error code.
*2: The C/R waits “initial reset “( “00”, “01”, “02”, “04” ,”05” and “06”) command after the HOST received the
error code.
*3: HOST can sent a next command after HOST received the error code. But the HOST shall activate ICC after
deactivation.
*4: If ICC reference standard is “ISO”, C/R doesn’t deactivate automatically. HOST should execute
deactivate or warm reset after HOST received the error code.
If ICC reference standard is “EMV3.0 Errata 1.0” or “Europay”, C/R deactivates automatically. HOST
should tries again to activate after HOST received the error code.


4 Command Parameters

```
4.1 Initial Setting Data (0~2 bytes)
The data items ( order ) for 1 and 2 can be omitted.
```
```
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
10-1 "0" 10ms *1
"2"~"9" 20ms~90ms
```
```
Minimum Guaranteed Time of switching between sending
and receiving *2
"A" Hold inside the C/R
"B" Return to front *1
```
##### 20-1

```
"C" Eject to Rear
```
```
Card Processing Method After Power Failure
```
```
*1: Indicates the default value.
*2: Minimum Guaranteed Time of switching between sending and receiving means minimum time until
the C/R send the Response ( DEL-ACK or response ) after the C/R received a Command or DEL-
ENQ from the HOST.
```
```
4.2 Track Number A (1 byte)
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
"1" ISO #1
"2" ISO #2
"3" ISO #3
"4" ISO #1 + ISO #2
"5" ISO #1 + ISO #3
"6" ISO #2 + ISO #3
```
##### 11

##### "7" ISO #1 + ISO #2 + ISO #3

```
Note: Designation of Multiple Track can be performed.
```
```
4.3 Track Number B (1 byte)
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
"1" ISO #1
"2" ISO #2
```
##### 11

##### "3" ISO #3

```
Note: Designation of Multiple Track can’t be performed.
```
```
4.4 Magnetic data A (1~104 bytes )
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
1-76 Card Data ISO #1
1-37 Card Data ISO #2
```
##### 1

```
1-104 Card Data ISO #3
```
```
Magnetic Data
```
```
See Annex B
```
```
4.5 Magnetic Data B (2~105 bytes)
Order Length
(Bytes)
```
```
Data
(ASCII)
Meaning
"1" ISO #1
"2" ISO #2
```
##### 11

##### "3" ISO #3

```
Track No.
```
```
1-76 Card Data ISO #1
1-37 Card Data ISO #2
```
##### 2

```
1-104 Card Data ISO #3
```
```
Magnetic Data
```
```
See Annex B
```

```
4.6 Magnetic Data C (2~105 bytes)
Magnetic data C is made up track number to be specified and magnetic data to be write.
When multiple tracks are specified ( in case “4”,”5”,”6” and “7” of data ) , card data corresponded the track
of [ ] should be set. And magnetic data of other track(s) should be set by Command ("78") in advance.
But, magnetic data is able to omit in case that write all track(s) data had already been set.
```
```
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
"1" ISO #1
"2" ISO #2
"3" ISO #3
"4" [ISO #1]+ISO #2
"5" [ISO #1]+ISO #3
"6" [ISO #2]+ISO #3
```
##### 11

##### "7" [ISO #1]+ISO #2+ISO #3

```
Track No.
```
```
1-76 Card Data ISO #1
1-37 Card Data ISO #2
```
##### 2

```
1-104 Card Data ISO #3
```
```
Magnetic Data
```
```
See Annex B
```
```
4.7 Retry Number (1 byte)
Data (ASCII)
Default value by
command
```
```
Meaning
Order Length
(Bytes) Value unit
"R0" "R1" ÅÅÅÅ Command “Code”
1 1 “0”-“9” No. “1” “1” Retry no.
```
```
4.8 Return Retry Number ( 2 bytes)
Data (ASCII) Meaning
Order
Length
(Bytes) Value unit Default value ÅÅÅÅ Command “Code”
12 “ 00 ”-“ 99 ” No. “ 03 ” Retry no.
```
```
4.9 Monitoring Time Data (2 bytes)
Data (ASCII)
Default value by command
Meaning
Order
Length
(Bytes) Value unit
"W0" "W1" “W2” ÅÅÅÅ Command “Code”
```
(^12) “ (^00) ”-“ (^99) ” Seconds “ (^30) ”“ (^30) ”“ (^10) ” Monitoring Time ( "00": Waits infinitely )
Note: For Command details, see 3.3.1 -(1).
4.10 P/F Condenser Existence (1 byte)
Designates attaching of the P/F condenser.
Order Length
(Bytes)
Data
(ASCII)
Meaning
11 "0" *1 Without P/F condenser
"1" With P/F condenser
*1: Shows the default value.


```
4.11 Magnetic head type ( 3 bytes )
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
11 “ 0 ”“ 1 ”“ 2 ”
Without ISO #1 With ISO #1 read With ISO #1 read/write
```
```
ISO #1 head type
```
##### 21 “ 0 ”“ 1 ”“ 2 ”

```
Without ISO #2 With ISO #2 read With ISO #2 read/write
```
```
ISO #2 head type
```
##### 31 “ 0 ”“ 1 ”“ 2 ”

```
Without ISO #3 With ISO #3 read With ISO #3 read/write
```
```
ISO #3 head type
```
4.12 I/O ports using (1 byte)
Designates using of the I/O port.

```
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
11 "0" No using I/O port
"1" *1 Using I/O port
*1: Indicates default setting.
```
```
4.13 Execution Designation Data (1 byte)
Data
(ASCII)
Default value by command
Order
Length
(Bytes) Value
“D0” “D1” “D2” “D3” “D4” “D5” “D6” “D7”
```
```
Meaning
```
```
ÅÅÅÅCommand “Code”
11 “0” -- *1 -- *1 -- *1 -- *1 Doesn’t execute
“1” *1--*1--*1--*1--Executes
*1: It shows the setting as default value for each command.
```
```
4.14 Transmission Format of Magnetic Data (1 byte)
The HOST designates Magnetic Data Format of the Sending and Receiving with the Command or
Response. The Default value is set in case of no designation.
```
```
Order Length
(Bytes)
```
```
Data
(ASCII)
```
```
Meaning
```
```
"0" *1 Only Data
"1" SS, Data, ES
```
##### 11

```
"2" SS, Data, ES, LRC
*1 Indicates default value
```
```
The HOST can select the format based on Processing Method of the Magnetic Data by application of the
HOST. The Parameters (Write Data) of Write Command and the responses of Read Commands (Read
Data) are shown in the table below.
```
```
Format "0" (default) “ 1 ” “ 2 ”
designation Only Data SS, Data, ES SS, Data, ES, LRC
Data length
Track
```
```
Minimum
Length (bytes)
```
```
Maximum
Length (bytes)
```
```
Minimum
Length (bytes)
```
```
Maximum
Length (bytes)
```
```
Minimum
Length (bytes)
```
```
Maximum
Length (bytes)
ISO #1176378479
ISO #2137339440
ISO #3 1 104 3 106 4 107
```

4.15 Magnetic Format (7 bytes)
Commands is used for Read or Write of Magnetic Data Formats outside of the standard. After setting,
set format of Read or Write is executed until this command is set again by another data or the C/R power
is turned OFF-ON.

```
Data (ASCII)
Order Default value ( Standard value )
Length
(Bytes)
ISO #1 ISO #2 ISO #3
```
```
Meaning
```
##### “^1 ” -- -- -- ISO #1

##### “ 2 ” -- -- -- ISO #2

##### 11

##### “ 3 ” -- -- -- ISO #3

```
Track No.
```
```
“ 5 ” -- *1 *1 5 bits
“ 6 ” -- -- -- 6 bits
“ 7 ” *1 -- -- 7 bits
```
##### 21

```
“ 8 ” -- -- -- 8 bits
```
```
Character Length
```
```
“E” -- -- -- Even Parity
“O” *1 *1 *1 Odd Parity
```
##### 31

```
“N” -- -- -- Without Parity
```
```
Vertical Parity Calculation
Method
```
```
“ 0 ” *1 *1 *1 Even LRC
“ 1 ” -- -- -- Even LRC-2
“ 2 ” -- -- -- Odd LRC
“ 3 ” -- -- -- CRC
“ 4 ” -- -- -- CRC-2
“ 5 ” -- -- -- CRC-3
```
##### 41

##### “ 6 ” -- -- -- CRC-4

```
Longitudinal Calculation
Method *2
```
```
5 1 ASCII “sp”“ 0 ”“ 0 ” Top Character
6 1 ASCII “%”“;”“;” SS Character
7 1 ASCII “?”“?”“?” ES Character
*1: Indicates default value
*2: LRC/CRC Calculation Method is shown below.
```
```
No. Name Check Range Storage Position Check Code Remarks
"0" Even LRC SS~ES After ES 1 Character --
"1" Even LRC-2 After SS~ES After ES 1 Character --
"2" Odd LRC SS~ES After ES 1 Character --
"3" CRC SS~ES After ES 2 Character X^16+X^12+X^5+X^1
"4" CRC-2 After SS~ES After ES 2 Character X^16+X^12+X^5+X^1
"5" CRC-3 SS~ES After ES 2 Character X^16+X^15+X^2+X^1
"6" CRC-4 After SS~ES After ES 2 Character X^16+X^15+X^2+X^1
```
```
Combinations of Character Length, Vertical Parity Calculation, and Longitudinal Parity Calculation are
shown in table below.
(“O” shows Enabling and “X” shows disabling )
```
```
Character Longitudinal Calculation Method
Length
```
```
Vertical Parity
Calculation Method Even LRC Even LRC-2 Odd LRC CRC CRC-2 CRC-3 CRC-4
8 Without Parity X X X OOOO
7 Odd Parity O O O XXXX
Even Parity O O O XXXX
6 Odd Parity O O O XXXX
Even Parity O O O XXXX
5 Odd Parity O O O XXXX
Even Parity O O O XXXX
```

4.16 Start Sentinel (SS) Positioning Data (3 bytes)
Data (ASCII)
Order
Length
(Bytes) Value Unit
Default
value

```
Meaning
```
```
“ 1 ” -- -- ISO #1
“ 2 ” -- -- ISO #2
```
##### 11

##### “ 3 ” -- -- ISO #3

```
Track No.
```
(^22) “-5”-“ (^22) ” mm “ (^00) ” *1
*1: The standard value (default value) of supplementary Data for Write Start Position of the Start Sentinel
is 7.4mm. For example, in the case of "05", 5mm + 7.4mm = 12.4mm.
4.17 Node Address (0 or 2 byte)
Data (ASCII)
Order
Length
(Bytes) Value Default value Meaning
1 0-1 “ 0 ”-“ 7 ”“ 0 ” NAD (Node Address) of ICC
0-1 “ 0 ”-“ 7 ”“ 0 ” NAD of C/R
For details, see ISO/IEC 7816-3 Amd.1.
4.18 PTS/NAD setting (1 or 3 bytes)
Data(ASCII)
Order
Length
(Bytes) Value Default
Value
Meaning
11 “ 0 ” -- C/R executes PTS automatically after ATR receiving
“ 1 ” -- C/R doesn’t executes PTS automatically after ATR receiving
20~1“ 0 ”~“ 7 ”“ 0 ” NAD (Node Address) of the ICC
30~1“ 0 ”~“ 7 ”“ 0 ” NAD of C/R


```
4.19 T=0 (Character Transmission Type) Transmission Data ( 4-261 bytes )
Order Code Name Length Description Remarks
1
2
3
4
```
##### CLA

##### INS

##### P1

##### P2

```
Class
Instruction
Parameter 1
Parameter 2
```
##### 1

##### 1

##### 1

##### 1

```
Class of instruction
Instruction code
Instruction parameter 1
Instruction parameter 2
```
##### --

```
5 Lc field Length variable =3 Number of byte(s) present in the data
field of the command
```
```
Executes only in case of
Length =< 1
6Data
field
```
```
Data variable = Lc String of byte(s) is sent in the data field
of the command
```
##### --

```
7 Le field Length variable =< 3 Maximum number of byte(s) expected
in the data field of the response to the
command
```
```
Executes only in case of
Length =< 1
```
```
For details, see ISO/ICE 7816-4. But following case 1 to case 4 of table below is able to use.
```
```
ISO/IEC 7816-4: Annex A Transportation of APDUs by T=0 Remarks
A.1 Case 1 Enable
Case 2S.1 Accepted Le Enable
Case 2S.2 Definitely not accepted Le Enable
```
```
A.2 Case 2 short
```
```
Case 2S.3 Not accepted Le, indicated La *1
A.3 Case 3 short Enable
Case 4S.1 Not accepted Command *1
Case 4S.2 Accepted Command *1
```
```
A.4 Case 4 short
```
Case 4S.3 Accepted Command with information added *1
A.5 Case 2 Extended Disable
A.6 Case 3 Extended Disable
A.7 Case 4 Extended Disable
*1: It is enabled to use only when ICC reference standard is only “EMV3.0”.

```
4.20 T=1(Block Transmission Type) Transmission Data (4~360 bytes)
Only Information Field(INF: order 1-7) should be set in the Transmission Data as T=1 Protocol Prologue
Field(NAD, PCB, LEN) and Epilogue Field(EDC) are automatically added in the C/R side.
```
```
Order Code Name Length Description Remarks
1
2
3
4
```
##### CLA

##### INS

##### P1

##### P2

```
Class
Instruction
Parameter 1
Parameter 2
```
##### 1

##### 1

##### 1

##### 1

```
Class of instruction
Instruction code
Instruction parameter 1
Instruction parameter 2
5 Lc field Length variable =3 Number of byte(s) presents in the data field of
the command
```
##### *1

```
6 Data field Data variable = Lc String of byte(s) is sent in the data field of the
command
7 Le field Length variable =< 3 Maximum number of byte(s) expected in the
data field of the response to the command
*1: The data length is either 0, 1 or 3.
For details, see ISO/ICE 7816-4 Annex B Transportation of APDUs by T=1.
```

4.21 T=1(Block Transmission Type) Extended Transmission Data (5~360 bytes)
Only Information Field(INF: order 1-5 ) should be set in the Transmission Data as T=1 Protocol Prologue
Field(NAD, PCB, LEN) and Epilogue Field(EDC) are automatically added in the C/R side.

```
ISO/IEC 7816-4:1995 Table 6 Command APDU contents
Order Code Name Length Description
```
```
Remarks
```
```
1 CLA Class 1 Class of instruction
2 INS Instruction 1 Instruction code
3 P1 Parameter 1 1 Instruction parameter 1
4 P2 Parameter 2 1 Instruction parameter 2
5 Data field Data 1~356 String of byte(s) sent in the data field of the
command
```
4.22 Protocol type of PTS (1 byte)

```
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
11 "0" Selection of protocol type T=0.
"1" Selection of protocol type T=1.
For details, see ISO/IEC 7816-3.4.9.
```
4.23 The Number of Down load Block ( 23 bytes )

```
Order Length
(Bytes)
Data (ASCII) Meaning
1 12 “AAAAAAAAAAAA” Type of CPU
2 2 “AA” Firm Ware version of CPU
3 6 “000000” ~ ”FFFFFF” SUM Value of CPU ROM
4 3 “001”~192” Block no. to be down loaded
```
4.24 Down load Data ( 2054 bytes )

```
Order
Length
(Bytes) Data Meaning
11 ‘0’ ‘1’ ‘2’
Start Block Data Block(s) End Block
```
```
Block Identification Code
```
```
2 1 BIN Block Number
3 2048 BIN Data
4 4 BIN Data SUM Value
Note: This table shows Data construction when new FW is offered, and shows only information for
customer as no data processing by the HOST.
```
4.25 Output port setting (2~16 bytes)

```
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
“01” Port No.1
“02” Port No.2
“03” Port No.3
“04” Port No.4
“05” Port No.5
“06” Port No.6
“07” Port No.7
```
##### 12~16

```
“08” Port No.8
Note: Data except “01”-“08” is ignored.
```

4.26 Memory size of “USER” information ( 3 bytes )
Data(ASCII)
Order Length
(Bytes) Value unit
Meaning

```
13 “ 001 ”~“ 256 ” Bytes Size of “USER” information. ( size of Response )
```
4.27 Output port setting time ( 4~30 bytes)
The designated I/O port number and time should be set as pair. The order of I/O port number isn’t
required.
The error of setting time is +0 ms to -10 ms.
Data(ASCII)
Order Default value by command
Length
(Bytes) Value Unit
“T0” or “T1” “T2” or “T3”

```
Meaning
```
```
1 2 “0x” *1 -- --- -- I/O port number
2 2 “01”~”99” 100ms “10” “05” Time
3 2 “0x” *1 -- --- -- I/O port number
4 2 “01”~”99” 100ms “10” “05” Time
:: : : : : :
15 2 “0x” *1 -- --- -- I/O port number
16 2 “01”~”99” 100ms “10” “05” Time
*1: Data except “1”-“8” is ignored.
```
4.28 ICC Reference Standard(2 bytes)

```
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
“00” ISO (default)
“01” EMV 3.0 Errata 1.0
```
##### 12

```
“05” Europay (EMV 3.1.1)
```
4.29 Timer Value for Waiting for Reception (2 bytes)
Data(ASCII)
Order
Length
(Bytes) Value Default value Unit
Meaning

```
1 2 "06" - ”99” “10” Seconds Timer value of waiting for reception
from ICC
```
4.30 IFSD Control Method(1 byte)

```
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
11 "0" Requests IFSD automatically.(default)
"1" Not request IFSD.
```
4.31 TCK Control Method(1 byte)

```
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
11 "0" Checks TCK.(default)
"1" Not check TCK.
```

### 5.19 ICC Control Information(16 bytes) 5-

```
Data(ASCII)
Order
Length
(Bytes) Value Default value Unit
Meaning
1 2 "06" - ”99” “10” Seconds Timer value of waiting for reception
from ICC
2 2 “00” -- -- Spare
3 2 “00” -- -- Spare
4 2 “00” -- -- Spare
```

5 Response Data

```
5.1 Sensor Information (12 bytes)
Data(ASCII)
Order Length
(Bytes) “0” “1” “2” “3”
Meaning
```
```
1 1 No Card is in Card is in - - Sensor S0
2 1 Spare - - - Extra
3 1 No Card is in Card is in - - Sensor S2
4 1 Spare - - - Extra
5 1 No Card is in Card is in - - Sensor S4
```
```
Card Position Sensor
```
```
6 1 Shutter Closed Shutter Opened - - Shutter Echo
7 1 Without Stripe With Stripe - - Magnetic Stripe Detection
8 1 No Card is in Card is in - - Width Detection
9 1 Release IC Contact IC Contact - - IC Contact Echo
10 1 ICC Deactivation Pressed - - ICC Activation
11 1 Stop 1st speed 2nd speed 3rd speed Status of Motor
12 1 Spare - - - Extra
```
```
5.2 Magnetic Data D (1~104 bytes)
```
```
Order
Length
(Bytes)
```
```
Data
(ASCII) Meaning
1~76 Card Data ISO #1
1~37 Card Data ISO #2
```
##### 1

```
1~104 Card Data ISO #3
```
```
Magnetic Data
See Annex B
```
```
5.3 Magnetic Data E (2~105 bytes)
Magnetic Data E is consisted of those read Track(s) No. and Magnetic Data which was read correctly.
The HOST can find the Track Number which was read correctly by checking Data (as shown in order 1).
Magnetic Data in order 2 is the read data of the lowest track among the Track Number which was read
correctly in case of Multiple Tracks Read. And the read data of the other tracks should be read by using of
command "69".
```
```
Order Length
(Bytes)
```
```
Data
(ASCII)
Meaning
“ 1 ” ISO #1
“ 2 ” ISO #2
“ 3 ” ISO #3
“ 4 ” ISO #1 + ISO #2
“ 5 ” ISO #1 + ISO #3
“ 6 ” ISO #2 + ISO #3
```
##### 11

##### “ 7 ” ISO #1 + ISO #2 + ISO #3

```
Read Track Number
```
```
1~76 Card Data ISO #1
1~37 Card Data ISO #2
```
##### 2

```
1~104 Card Data ISO #3
```
```
Magnetic Data
```
```
See Annex B
```

5.4 Magnetic data F (6 ~233 bytes )
Magnetic data F is consisted of Track no.( Order 1 ), Result of read (Order 2-4), Length of Magnetic Data
( Order 5-7 ) and Magnetic Data ( Order 8-10 ) by designated read command "6A".

```
(1) The data of track that doesn't be designated by the command doesn't contain.
(2) Result of read by designated command is set "00" in case the track(s) data is normality, and is set
error code "4x", in chapter 3.4.2 , in case the data is abnormality.
```
```
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
11 “ 1 ”~” 7 ” Designated track number by command. Refer to 4.2.
2 0 or 2 result of reading ISO #1
3 0 or 2 result of reading ISO #2
4 0 or 2 result of reading ISO #3
```
```
None order : none data
Magnetic data normality : “ 00 ”
Magnetic data abnormality : see 3.4.2
5 0 or 3 Length ISO #1
6 0 or 3 Length ISO #2
7 0 or 3 Length ISO #3
```
```
None designating : none data
Magnetic data normality : Magnetic Data Length
Magnetic data abnormality : “ 000 ”
8 0~76 Card Data ISO #1
9 0~37 Card Data ISO #2
10 0~104 Card Data ISO #3
```
```
None designating : none data
Magnetic data normality : See Annex B
Magnetic data abnormality : No data
```
5.5 Error Track Number (0~1 byte)
The Error track Number is only sent to the HOST when an error occurred by Write Command.

```
Order
Length
(Bytes)
```
```
Data
(ASCII) Meaning
“^1 ” ISO #1
“ 2 ” ISO #2
“^3 ” ISO #3
“ 4 ” ISO #1 + ISO #2
“^5 ” ISO #1 + ISO #3
“ 6 ” ISO #2 + ISO #3
```
##### 11

##### “ 7 ” ISO #1 + ISO #2 + ISO #3

5.6 Captured Number of Card(s) (3 bytes)

```
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
13 “ 000 ”~” 999 ” Captured Number of Card
```
### 5.8 Option Information (16 bytes) 5-

```
Sensor voltage is transmitted as a numerical value data in units of 0.1 V from "00"~"50" for the Sensor
voltage level.
(Example) 4.8V -> "48"
```
```
Order
Length
(Bytes)
```
```
Data
(ASCII) Meaning
```
(^12) “ (^00) ”~” (^50) ” 0.0~5.0V Sensor S0
2 2 Spare - Extra
(^32) “ (^00) ”~” (^50) ” 0.0~5.0V Sensor S2
4 2 Spare - Extra
(^52) “ (^00) ”~” (^50) ” 0.0~5.0V Sensor S4
6 2 Spare - Extra
7 2 Spare - Extra
8 2 Spare - Extra
Sensor Voltage


5.8 Option Information (16 bytes)
Data(ASCII)
Order Length
(Bytes) “0” “1” “2” “?”
Meaning

```
1 1 Without shutter With shutter - - Shutter existence
2 1 Without IC
Contact
```
```
With IC Contact - - IC contact existence
```
```
3 1 Spare - - - Spare
4 1 Without ISO #1 With ISO #1
read
```
```
With ISO #1
read/write
```
```
No setting ISO #1 head specs.
```
```
5 1 Without ISO #2 With ISO #2
read
```
```
With ISO #2
read/write
```
```
No setting ISO #2 head specs.
```
```
6 1 Without ISO #3 With ISO #3
read
```
```
With ISO #3
read/write
```
```
No setting ISO #3 head specs.
```
```
7 1 Without P/F
condenser
```
```
With P/F
condenser
```
- No setting P/F condenser existence

```
8 1 Without extended
ROM
```
```
Spare - - Spare
```
```
9 1 Spare With Memory - - Memory existence
10 1 No using I/O ports Using I/O ports - No setting I/O port(s) using
11~16 6 spare - - No setting Spare
```
### 5.9 Version Information (40 bytes) 5-

```
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
112 “AAAAAAAAAAAA” CPU FW type
22 “AA” CPU FW Version
36 “ 000000 ”~”FFFFFF” CPU ROM SUM Value
4 12 Spare Spare
5 2 Spare Spare
6 6 Spare Spare
```
(^712) “AAAAAAAAAAAA” FW type in Memory
82 “AA” FW Version in Memory
(^98) “ (^00000000) ”~”FFFFFFFF” SUM Value in Memory

### 5.10 ATR (Answer to Reset) Information (2~33 bytes) 5-

```
Order Length
(Bytes)
```
```
Data
(BIN)
Meaning
1 1 00H-FFH TS Initial Character
2 1 00H-FFH T0 Format Character
3 Undefined 00H-FFH TA1~TDn Interface Character
4 0~15 00H-FFH T1~Tk Historical Characters
5
```
##### 0~31

```
0~1 00H-FFH TCK Check Character
For details, see ISO/IEC 7816-3.
```

### 5.11 ATR/PTS Information(3~34 bytes) 5-

```
Order
Length
(Bytes)
Data Meaning
“ 0 ” Enables to execute protocol type T=0 immediately.
“ 1 ” Enables to execute protocol type T=1 immediately.
“P” Needs to select protocol type by PTS Request Commands.
“N” Incompletion of PTS Execution
```
##### 11

```
“?” Command Parameter is “ No PTS Execution automatically.
2 1 00H-FFH TS Initial Character
3 1 00H-FFH T0 Format Character
4 Undefined 00H-FFH TA1~TDn Interface Character
5 0~15 00H-FFH T1~Tk Historical Characters
6
```
##### 0~31

```
0~1 00H-FFH TCK Check Character
```
### 5.12 T=0 ( Character Transmission Type ) Reception Data ( 2~258 bytes) 5-

```
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
1 0~256 ICC Data INF ICC Data (Information Field)
2 1 ICC Data SW1 Status-1
3 1 ICC Data SW2 Status-2
For details, see ISO/IEC 7816-4.
```
### 5.13 T=1 ( Block Transmission Type) Reception Data (2~320 bytes) 5-

```
Only Information Field ( INF) is returned as the received data after T=I Protocol Prologue Field ( NAD,
PCB, LEN ) and Epilogue Field (EDC) was deleted in the C/R side.
```
```
Order Length
(Bytes)
```
```
Data
(ASCII)
Meaning
1 0~318 ICC Data INF IC Card Data (Information Field)
2 1 ICC Data SW1 Status-1
3 1 ICC Data SW2 Status-2
For details, see ISO/IEC 7816-4.
```
### 5.14 PTS Information (1 byte) 5-

```
Order Length
(Bytes)
```
```
Data
(ASCII)
Meaning
“ 0 ” Enable to execute T=0.
“ 1 ” Enable to execute T=1.
```
##### 11

```
“N” Incompletion PTS Execution.
```
### 5.15 Memory Version Information (22 bytes) 5-

```
Order Length
(Bytes)
```
```
Data
(ASCII)
Meaning
112 “AAAAAAAAAAAA” FW type in Memory
```
(^22) “AA” FW Version in Memory
38 “ 00000000 ”~”FFFFFFFF” SUM Value in Memory


### 5.16 USER Information in memory (1~256 bytes) 5-

```
C/R sends response data of length specified by the command parameter.
```
```
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
1 1-256 ASCII Read data in USER memory
```
### 5.17 Input port Information ( 4bytes) 5-

```
Order
Length
(Bytes)
```
```
Data
(ASCII)
Meaning
11 “ 0 ” Input Port No.1 is OFF.
“ 1 ” Input Port No.1 is ON.
21 “ 0 ” Input Port No.2 is OFF.
“ 1 ” Input Port No.2 is ON.
31 “ 0 ” Input Port No.3 is OFF.
“ 1 ” Input Port No.3 is ON.
41 “ 0 ” Input Port No.4 is OFF.
“ 1 ” Input Port No.4 is ON.
```
### 5.18 FW Version Information of Nonvolatile Memory(22 bytes) 5-

```
Order
Length
(Bytes)
```
```
Data
(ASCII) Meaning
```
(^112) “AAAAAAAAAAAA” *1 FW type of nonvolatile memory
22 “AA” *1 FW version of nonvolatile memory
(^38) “ (^000000) ”~”FFFFFF” *2 FW SUM value of nonvolatile memory
*1 In case of incomplete program, “_” is indicated. “_” denotes 20H of HEX code.
*2 In case of incomplete program, “0” is indicated.
5.19 ICC Control Information(16 bytes)
Order
Length
(Bytes)
Data
(ASCII)
Meaning
“00” ISO (default)
“01” EMV 3.0 Errata 1.0

##### 12

```
“05” Europay (EMV 3.1.1)
2 2 "06" - ”99” Timer value of waiting for reception from ICC ( Unit: seconds)
31 "0" Requests IFSD automatically.
"1" Not request IFSD.
41 "0" Checks TCK.
"1" Not check TCK.
5 10 “0” Spare
```

