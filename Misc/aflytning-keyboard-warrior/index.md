+++
title = 'Aflytning: keyboard warrior'
categories = ['Misc']
date = 2023-12-17T20:37:16+01:00
scrollToTop = true
+++

## Challenge Name:

Aflytning: keyboard warrior

## Category:

Misc

## Challenge Description:
```text
Vi har troværdige efterretninger der peger på, at nissedev er indblandet i udviklingen af Nisseware!

Ved en hemmelig ransagning har vi installeret aflytning af hans trådløse devices. Kan du decode den aflyttede data og identificere hans rolle?

*Nissedev bruger altid amerikansk tastaturlayout*
```


## Approach

We're given a [file named "keyboard.pcapng"](scripts/keyboard.pcapng)

Pcapng is the "Packet Capture next generation" format, which is the standard format for any programs saving network packages.
Most often, the captures are based on NICs (Network interfaces), and the traffic flowing through them, but in this file, it's a bunch of USB packets instead.

As the title and description suggest, we're supposed to figure out what the elf is writing on his keyboard, and we're even told that the layout is American.

.pcap and .pcapng files are most easily explored using [Wireshark](https://www.wireshark.org/), or via the CLI with [t-shark](https://www.wireshark.org/docs/man-pages/tshark.html).

Our first task is figuring out which USB device is the keyboard.

If we open the file in Wireshark and take a look at the packets captured, it neatly starts out with a bunch of DESCRIPTOR packages.
We can see there's 4 USB devices involved:
```text
3.1.0
3.2.0
3.4.0
3.14.0
```

Looking into the descriptor packages for each devices, shows us who made it and its product name:
![](images/descriptor-packet.png)

Looking at all 4 devices, we're left with this:
```text
3.1.0 = 
    * idVendor: Linux Foundation
    * idProduct: 2.0 root hub
    * bDeviceProtocol: Hi-speed hub with single TT
Conclusion: a USB hub, candidate for having a Keyboard attached

3.2.0
    * idVendor: Luxvisions Innotech Limited
    * idProduct: Unknown 
Conclusion: most likely a camera/webcam, based on the vendors product catalog.

3.4.0:
    * idVendor: Intel Corp
    * idProduct: AX211 Bluetooth
Conclusion: a bluetooth receiver


3.14.0 = Logitech Unifying receiver 
    * idVendor: Logitech, Inc.
    * idProduct: Unifying Receiver
Conclusion: a logitech unifying receiver, which can be connected to (multiple) mice and/or keyboards.
```

So we're down to two possible candidates. A keyboard stroke will always be sent as as URB_INTERRUPT [USB Request Block interrupt](https://docs.kernel.org/driver-api/usb/URB.html) packet. If we look at all packets of that type, the majority are from 3.14.3 (a sub-device on the unifying receiver), so best guess is, that's where we're focusing for this task.

Unfortunately there's no descriptor packages sent to/from 3.14.3, so we can't tell what device it is.

If we want to look at the actual keystroke being sent, we have to focus at one of two fields in Wireshark/tshark:
* `usb.capdata`
* `usbhid.data`

Which is used, is entirely dependent on the device sending the packets.
In our case, it seems like we're looking at `usbhid.data`, since a search for that provides 1870 packets, while `usb.capdata` gives 128.

Lets get those packets extracted, that's where t-shark comes in:
`tshark -r keyboard.pcapng -T fields -e usbhid.data > capdata.txt`

This gives us a file containing all keystrokes from the keyboard, in this format:
```text
200201000700000000000000000000
200201000000000000000000000000
200201000400000000000000000000
200201000000000000000000000000
200201000a00000000000000000000
200201000000000000000000000000
200201000500000000000000000000
```

Since this was my first time working with USB packets, I just started playing around with a python script, based on what I could find on the internet. Nothing matched perfectly (which I'm sure is on purpose from the creators), but I was able to figure out the structure pretty fast

Manually manipulating the data  down to the fields that actually change between lines, I was left with this format:
```text
020000
020e00
020000
000400
000800
001500
001508
000800
002c00
020000
...
```

The first byte is a modifier key. For example pressing shift, produces `020000`, whilst pressing another key with shift held down, produces `020e00`.

The second byte is the character key being pressed, the bytes matched almost all tables I found online (eg. `04 == a`), so I'm guessing its a standard for american keyboards.

The third character seems to be a repetition-marker. Every time its greater than 0, the key seems to be held down, and will be duplicated if transferred to the output.

Based on that, I wrote this very [rudimentary Python script](scripts/decode_keyboard_v1.py):

```python
import os

presses = []
with open(os.path.relpath("capdata.txt"), "r") as f:
    for line in f:
        presses.append(line[0:-1])

normalKeys = {"04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4", "22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"\t","2c":"<SPACE>","2d":"-","2e":"=","2f":"[","30":"]","31":"\\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}
shiftKeys = {"04":"A", "05":"B", "06":"C", "07":"D", "08":"E", "09":"F", "0a":"G", "0b":"H", "0c":"I", "0d":"J", "0e":"K", "0f":"L", "10":"M", "11":"N", "12":"O", "13":"P", "14":"Q", "15":"R", "16":"S", "17":"T", "18":"U", "19":"V", "1a":"W", "1b":"X", "1c":"Y", "1d":"Z","1e":"!", "1f":"@", "20":"#", "21":"$", "22":"%", "23":"^","24":"&","25":"*","26":"(","27":")","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"\t","2c":"<SPACE>","2d":"_","2e":"+","2f":"{","30":"}","31":"|","32":"<NON>","33":":","34":"\"","35":"<GA>","36":"<","37":">","38":"?","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}

def main():
    result = ""
    for press in presses:
        bytes = [press[i:i+2] for i in range(0, len(press), 2)]

        if bytes[1] == "00" or bytes[2] != "00":
            continue
    
        if bytes[0] == "02":
            result += shiftKeys[bytes[1]]
        else:
            result += normalKeys[bytes[1]]

    print("[+] Found : %s" % (result))

if __name__ == "__main__":
    main()
```

Which produces this output:
```
Kaere<SPACE>Nissedagbog!<RET><RET>I<SPACE>dag<SPACE>har<SPACE>jeg<SPACE>vaeret<SPACE>paa<SPACE>besoeg<SPACE>hos<SPACE>Hhr.<SPACE>Mortensen<SPACE>for<SPACE>at<SPACE>laere<SPACE>mere<SPACE>om<SPACE>udvikling<SPACE>ad<SPACE><DEL><DEL>f<SPACE>ransoma<DEL>ware<DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL>betalingsplatforme<DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL>kundeorienterede<SPACE>loesninger.<RET>Det<SPACE>er<SPACE>super<SPACE>kedeligt<DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL>spaendende,<SPACE>og<SPACE>jeg<SPACE>laerer<SPACE>en<SPACE>HEL<SPACE>masse,<SPACE>jeg<SPACE>ikke<SPACE>vidsee<DEL><DEL>te<SPACE>foer!<RET><RET>I<SPACE>morgen<SPACE>skal<SPACE>jeg<SPACE>paa<SPACE>besoeg<SPACE>hos<SPACE>Nnissefar,<SPACE>saa<SPACE>de<SPACE>kan<SPACE>teste<SPACE>om<SPACE>jeg<SPACE>allerede<SPACE>nu<SPACE>er<SPACE>klar<SPACE>til<SPACE>at<SPACE>komme<SPACE>paa<SPACE>udviklerholdet!<RET>Det<SPACE>ville<SPACE>vaere<SPACE>ret<SPACE>cool<SPACE>at<SPACE>vaere<SPACE>medudvikler<SPACE>paa<SPACE>et<SPACE>saa<SPACE>indbringende<SPACE>produl<DEL>kt!<RET>Maaske<SPACE>jeg<SPACE>endda<SPACE>kan<SPACE>gaa<SPACE>selvstaendig<SPACE>og<SPACE>r<DEL>tjene<SPACE>en<SPACE>masse<SPACE>penge<SPACE>udeom<DEL><DEL>nom<SPACE>ding<SPACE><DEL><DEL><DEL><DEL>en<SPACE>naerrige<SPACE>nissefar!<DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL>Jjeg<SPACE>mener...<DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL><RET>Jjeg<SPACE>haaber<SPACE>det<SPACE>kommer<SPACE>til<SPACE>at<SPACE>gaa<SPACE>rigtig<SPACE>godt<SPACE>ale<DEL>t<SPACE>sammen!<RET><RET>NC3{alt<DEL><DEL><DEL>4lt_k<DEL><DEL><DEL><DEL><DEL>pas<DEL><DEL>4s_paa_hv4d_-du_skriver<DEL><DEL><DEL><DEL><DEL><DEL><DEL>5kr1v3r_n1ss3d3v_maaske_nogen<DEL><DEL><DEL><DEL>0ge<DEL>3n_foelger_med<DEL><DEL>3d!}<RET><RET>XOXO<SPACE>nissedev<RET>
```

While the text is obviously correct (it's danish), and with a bit of manual manipulation in the final part, the flag is easily retrievable, I had to go back and modify the script a bit.

If we replace `<SPACE>` with an actual space, and `<RET>` with a newline, then add a bit of handling for backspace:
```python
        if bytes[0] == "02":
            key = shiftKeys[bytes[1]]
        else:
            key = normalKeys[bytes[1]]
        
        if (key == "<DEL>"):
            result = result[:-1]
        else: 
            result +=key
```

The output text is a lot more legible:
```text
Kaere Nissedagbog!

I dag har jeg vaeret paa besoeg hos Hhr. Mortensen for at laere mere om udvikling af kundeorienterede loesninger.
Det er super spaendende, og jeg laerer en HEL masse, jeg ikke vidste foer!

I morgen skal jeg paa besoeg hos Nnissefar, saa de kan teste om jeg allerede nu er klar til at komme paa udviklerholdet!
Det ville vaere ret cool at vaere medudvikler paa et saa indbringende produkt!
J
Jjeg haaber det kommer til at gaa rigtig godt alt sammen!

NC3{p4s_paa_hv4d_-du_5kr1v3r_n1ss3d3v_maaske_n0g3n_foelger_m3d!}

XOXO nissedev
```
[Final script download](scripts/decode_keyboard_v2.py)

There's still a few duplicated characters in there, as well as a malplaced `-` in the flag, but overall i'm satisifed since the flag is easily readable. So I stopped working on the script here and moved on to the next task.

## Flag

```text
NC3{p4s_paa_hv4d_du_5kr1v3r_n1ss3d3v_maaske_n0g3n_foelger_m3d!}
```

## Reflections and Learnings
The task is a fanstic introduction on how USB packets work between a keyboard and computer.
I was "forced" to lookup several standards and definitions, just to figure out what I was looking at.

Once the basic understanding was in place, it became a pretty simple translation task.

While I'm sure there are nuances in the packet output that I missed, I grasped enough to get a legible text within a hours, after starting from absolut zero, while learning a lot on the way.

