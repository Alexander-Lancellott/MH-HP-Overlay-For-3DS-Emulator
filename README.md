<h1 align="center"> MH-HP-Overlay-For-3DS-Emulator </h1>

<div align="center">

  [![StaticBadge](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
  [![App](https://img.shields.io/badge/App-1.0.0-green)](https://github.com/Alexander-Lancellott/MH-HP-Overlay-For-3DS-Emulator)

</div>

## Description

A simple open-source HP overlay that I've developed for MH3U/3G, MH4U/4G, and MHXX in Python. This overlay is designed to be used with the [Citra](https://citra-emulator.com/) emulator and its variants, such as [Lime3DS](https://github.com/Lime3DS/Lime3DS) and [Citra-Enhanced](https://github.com/CitraEnhanced/citra) on their PC (Windows) versions.

Although I've conducted numerous tests, the overlay may still contain some bugs that I haven't detected. If you encounter any issues, I would appreciate it if you could report them by opening an issue and providing any evidence that allows for replication.

## Compatibility

I think I've managed to make the overlay compatible with all existing versions of each game, with or without their updates. Below is a list of the versions where I tested and confirmed that the overlay works correctly:

- MH3G (JPN) - 0004000000048100 - v0(default)
- MH3U (EUR) - 00040000000B1D00 - v0(default)
- MH3U (USA) - 00040000000AE400 - v0(default)
<br />

- MH4G (JPN) - 000400000011D700 - v0(default), v1.1 & v1.2
- MH4G (Taiwan) - 0004000000141A00 - v0(default) & v1.1
- MH4U (EUR) - 0004000000126100 - v0(default) & v1.1
- MH4U (USA) - 0004000000126300 - v0(default) & v1.1
<br />

- MHXX (JPN) - 0004000000197100 - v0(default), v1.1, v1.2, v1.3 & v1.4
- MHXX (Taiwan) - 00040000001B8100 - v0(default), v1.1, v1.2, v1.3 & v1.4

## How to use

To use the overlay, simply open the `MH-HP-Overlay.exe` file.

If one of the games from the [compatibility list](#compatibility) isn't running in the emulator, you will see a red message in the overlay console saying **No game running** and a countdown starting from 20 minutes. When the countdown reaches zero, the overlay will automatically close to save resources.

![No game running](https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/no_game_running.webp)

Otherwise, if one of the games from the [compatibility list](#compatibility) is running in the emulator, you will see a green message in the overlay console indicating which of the compatible games is currently running.

![Game running](https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/game_running.webp)

> [!IMPORTANT]
> If you see a red message in the overlay console that says `Couldn't connect to 3DS emulator server`, make sure the 3DS emulator you're using isn't blocked by [Windows Firewall rules](https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/rules?source=recommendations). Additionally, ensure that port `45987` on localhost isn't being used by another process. To check if the port is free, you can run the following command in **CMD** or **PowerShell** before starting a game in the emulator:
> ```
> netstat -ano | findstr 45987
> ```
> If no process is using the port, the command should return no results.

If everything works correctly, upon starting a hunting mission, you should see `labels` arranged one below the other, displaying the monster's name along with its HP in the top right corner of the game window.

<div align="center">

  ![Labels](https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/labels.png)

</div>

If you don't like the color of the overlay or its position in the top right corner of the window, go directly to the [Customize Overlay](#customize-overlay) section to edit it to your liking. However, I recommend that you continue reading this section first.

### Borderless screen system & Native full-screen mode

If you prefer using the emulator's full-screen mode, you will notice that the overlay isn't visible in this mode. To solve this, I developed a borderless screen system that is practically the same as the emulator's native full-screen mode. This system can be toggled on/off using a keyboard shortcut, which is set to `Ctrl + Alt + F` by default. To exit this mode, simply press the same shortcut again.

It is important not to confuse this shortcut with the emulator's native shortcut for switching to full-screen mode, which is usually `F11` by default. If you want to change the default keyboard shortcut for the overlay, you can do so by checking the [Hotkey](#hotkey) sub-section.

![Transition](https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/transition.gif)

Keep in mind that, by default, the target window is the emulator's `main` window. If you use the overlay's borderless screen system, you'll notice that the emulator's toolbar and bottom bar will still be visible. This differs from the emulator's native full-screen mode. If you want to achieve an identical full-screen experience or simply switch between the emulator's target windows, you should check the [Target Window](#target-window) sub-section.

<table>
  <tr align="center">
    <td>
      <strong>Native full-screen mode</strong>
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/native-fullscreen.webp"
        target="_blank">
        <img alt="Full-screen"
          src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/native-fullscreen.webp"
          style="min-width: 397.5px;" />
      </a>
    </td>
  </tr>
</table>
<table>
  <tr align="center">
    <td>
      <strong style="white-space: nowrap;">
        Borderless screen system
      </strong>
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/borderless.webp"
        target="_blank">
        <img alt="Borderless"
          src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/borderless.webp"
          style="min-width: 397.5px;" />
      </a>
    </td>
  </tr>
</table>

## Customize Overlay

Inside the root folder, there is a file called `config.ini`, which stores the values for options that can be edited using a text editor like [Notepad++](https://notepad-plus-plus.org/downloads/) to customize the overlay.

**It's important to close and reopen the overlay each time you edit this file for the changes to take effect.**

Below, you will find sub-sections dedicated to documenting each of the available options in the `config.ini`.

### Show Small Monsters

The `show_small_monsters` option in the `config.ini` file determines whether the overlay will display all monsters, including small ones. By default, this option is set to `true`.

To display only large monsters, change the value of `show_small_monsters` to `false`.

Remember to close and reopen the overlay after making changes to the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>
      show_small_monsters
    </td>
    <td>
      true
    </td>
    <td>
      boolean
    </td>
    <td>
      This is case-insensitive and recognizes boolean values from 'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0'
    </td>
  </tr>
</table>

### Hotkey

The `config.ini` file includes the `hotkey` option, which defines the keyboard shortcut used to toggle the borderless screen system on/off. By default, this shortcut is `Ctrl + Alt + F`. You can replace it with another shortcut if the default one is inconvenient for you.

It's important to note that special keys such as `Ctrl`, `Shift`, or `Alt` are represented by specific symbols. It's recommended to refer to the following [documentation](https://www.autohotkey.com/docs/v1/Hotkeys.htm#Symbols) to ensure you're using the correct symbols when editing the shortcut. The symbols `*`, `~`, `$` aren't allowed.

Remember to close and reopen the overlay after making changes to the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>hotkey</td>
    <td>^!f</td>
    <td>string</td>
    <td>
      Must be valid hotkey, check this: https://www.autohotkey.com/docs/v1/Hotkeys.htm#Symbols
    </td>
  </tr>
</table>

### HP update time

The `hp_update_time` option in the `config.ini` file allows you to adjust the refresh time of the HP value in seconds. By default, this value is set to `1` second, which is the minimum possible value.

You can modify this value to increase the time interval for refreshing the HP value. Higher values will increase the update interval, potentially reducing the frequency of HP value updates.

Remember to close and reopen the overlay after making changes to the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>hp_update_time</td>
    <td>1</td>
    <td>float</td>
    <td>Must be greater than or equal to 1</td>
  </tr>
</table>

### Font

Within the `config.ini` file, you can customize the type, weight, and size of the font used in the overlay by editing the following options:

- `font_family`: Allows you to change the font type. You should use fonts that are compatible with the web (**Web Safe Fonts**). You can find a list of these fonts [here](https://www.cssfontstack.com/).
<br />

- `font_weight`: Allows you to adjust the font weight. Common values include `normal` for regular weight and `bold` for bold weight.
<br />

- `font_size`: Allows you to specify the font size in pixels.

Make sure to use **Web Safe Fonts** and to close and reopen the overlay after making changes in the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>font_family</td>
    <td>Consolas, monaco, monospace</td>
    <td>string</td>
    <td>
      This is a <a href="https://developer.mozilla.org/en-US/docs/Web/CSS/font-family">CSS property</a> and must be a <a href="https://www.cssfontstack.com/">Web Safe Font</a>
    </td>
  </tr>
  <tr align="center">
    <td>font_weight</td>
    <td>bold</td>
    <td>string</td>
    <td>
      This is a <a href="https://developer.mozilla.org/en-US/docs/Web/CSS/font-weight">CSS property</a>
    </td>
  </tr>
  <tr align="center">
    <td>font_size</td>
    <td>18</td>
    <td>integer</td>
    <td>
      This is a <a href="https://developer.mozilla.org/en-US/docs/Web/CSS/font-size">CSS property</a>, its value is in pixels and must be greater than or equal to 1
    </td>
  </tr>
</table>

### Target window

Within the `config.ini` file, the `target_window` option allows the overlay to target one of the three available windows in the **Citra** emulator or its variants:

- `main`: This window includes the toolbar at the top and the bottom bar displaying FPS. It's the default configuration in the **Citra** emulator.
<br />

- `primary`: This window is separate from the toolbar and FPS bottom bar, presenting a clean window. It's the recommended option for use with the overlay's borderless screen system.
<br />

- `secondary`: This window is similar to the primary window but by default shows the secondary screen of the 3DS console. It'll only be visible if the **Screen Layout** option is set to **Separate Windows** within the emulator.

To view the primary window in the **Citra** emulator, follow these steps:

1. Go to the emulator's toolbar.
2. Click on **View**.
3. Disable the **Single Window Mode** option.

Remember to close and reopen the overlay after making changes to the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>target_window</td>
    <td>main</td>
    <td>string</td>
    <td>Must be main, primary or secondary</td>
  </tr>
</table>

<table>
  <tr align="center">
    <td>
      <strong>target_window = main</strong>
    </td>
  </tr>
  <tr align="center">
    <td>
        <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/main.webp" 
        target="_blank">
          <img alt="main"
          src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/main.webp"
          style="min-width: 397.5px;" />
        </a>
    </td>
  </tr>
</table>
<table>
  <tr align="center">
    <td>
        <strong>target_window = primary<strong>
    </td>
  </tr>
  <tr>
    <td>
        <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/primary.webp"
        target="_blank">
          <img alt="primary"
          src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/primary.webp"
          style="min-width: 397.5px;" />
        </a>
    </td>
  </tr>
</table>
<table>
  <tr align="center">
    <td>
      <strong>target_window = secondary<strong>
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/secondary.webp"
      target="_blank">
        <img alt="secondary"
        src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/secondary.webp"
        style="min-width: 397.5px;" />
      </a>
    </td>
  </tr>
</table>

### Align

Within the `config.ini` file, the `align` option controls the alignment of labels in the overlay. When set to `true`, all labels will adjust their width to match the width of the largest label.

This ensures a consistent and orderly presentation of labels in the overlay interface.

Remember to close and reopen the overlay after making changes to the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>align</td>
    <td>true</td>
    <td>boolean</td>
    <td>
      This is case-insensitive and recognizes boolean values from 'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0'
    </td>
  </tr>
</table>

<table>
  <tr align="center">
    <td>
      <strong>align = true</strong>
    </td>
    <td>
      <strong>align = false</strong>
    </td>
  </tr>
  <tr>
    <td>
        <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/labels.webp"
        target="_blank">
          <img alt="labels"
          src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/labels.webp" />
        </a>
    </td>
    <td>
      <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/align.webp"
      target="_blank">
        <img alt="align"
        src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/align.webp" />
      </a>
    </td>
  </tr>
</table>

### Orientation

The `orientation` option within the `config.ini` file allows you to define the position of content within the `labels`. You can configure this option with one of the following values:

- `center`: Centers the content within the `labels`.
<br />

- `left`: Aligns the content to the left within the `labels`.
<br />

- `right`: Aligns the content to the right within the `labels`.

Remember to close and reopen the overlay after making changes in the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>orientation</td>
    <td>center</td>
    <td>string</td>
    <td>Must be center, left or right</td>
  </tr>
</table>

<table>
  <tr align="center">
    <td colspan="2">
      <strong>align = true</strong>
    </td>
    <td>
      <strong>align = false</strong>
    </td>
  </tr>
  <tr align="center">
    <td>
      <strong>orientation = center</strong>
    </td>
    <td>
      <strong>orientation = left</strong>
    </td>
    <td>
      <strong>orientation = right<strong>
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/labels.webp"
      target="_blank">
        <img alt="labels"
        src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/labels.webp" />
      </a>
    </td>
    <td>
      <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/left.webp"
      target="_blank">
        <img alt="left"
        src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/left.webp" />
      </a>
    </td>
    <td>
      <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/right.webp"
      target="_blank">
        <img alt="right"
        src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/right.webp" />
      </a>
    </td>
  </tr>
</table>

### Position (X & Y)

The `x` and `y` options within the `config.ini` file allow you to adjust the position of the overlay using Cartesian coordinates. These values are relative and percentage-based to the size of the target window, with a minimum range of `0` and maximum of `100` for each coordinate.

- `x`: Controls the horizontal position of the overlay.
<br />

- `y`: Controls the vertical position of the overlay.

Adjust these values to move the overlay to the desired position on the screen.

Remember to close and reopen the overlay after making changes in the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>x</td>
    <td>100</td>
    <td>integer</td>
    <td>Must be greater than or equal to 0 and less than or equal to 100</td>
  </tr>
  <tr align="center">
    <td>y</td>
    <td>0</td>
    <td>integer</td>
    <td>Must be greater than or equal to 0 and less than or equal to 100</td>
  </tr>
</table>

<table>
  <tr align="center">
    <td>
      <strong>x = 100</strong>
      <br/>
      <strong>y = 0</strong>
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/x-100.webp" 
      target="_blank">
        <img alt="x-100"
        src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/x-100.webp"
        style="min-width: 397.5px;" />
      </a>
    </td>
  </tr>
</table>
<table>
  <tr align="center">
    <td>
      <strong>x = 0<strong>
      <br/>
      <strong>y = 0<strong>
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/x-0.webp"
      target="_blank">
        <img alt="x-0"
        src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/x-0.webp"
        style="min-width: 397.5px;" />
      </a>
    </td>
  </tr>
</table>
<table>
  <tr align="center">
    <td>
      <strong>x = 0<strong>
      <br/>
      <strong>y = 100<strong>
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/y-100.webp"
      target="_blank">
        <img alt="y-100"
        src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/y-100.webp"
        style="min-width: 397.5px;" />
      </a>
    </td>
  </tr>
</table>

### Fix X & Fix Y

The `fix_x` and `fix_y` options within the `config.ini` file allow you to adjust the position of the overlay in specific situations where modifying the `x` and `y` coordinates may not be sufficient.

These options should only be modified in particular circumstances or when adjusting the `x` and `y` coordinates doesn't adequately resolve the overlay's location. For example, if you're using the `main` window target in emulators like **Lime3DS** or **Citra-Enhanced**, you may notice that the toolbar is thicker or taller than in Citra. In such cases, you should set the `fix_y` option to `10` to compensate for this difference.

Remember to close and reopen the overlay after making changes in the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>fix_x</td>
    <td>0</td>
    <td>integer</td>
    <td>It must be any integer, whether positive or negative, its value is in pixels</td>
  </tr>
  <tr align="center">
    <td>fix_y</td>
    <td>0</td>
    <td>integer</td>
    <td>It must be any integer, whether positive or negative, its value is in pixels</td>
  </tr>
</table>

<table>
  <tr align="center">
    <td colspan="2">
      <strong>In Lime3DS or Citra-Enhanced</strong>
    </td>
  </tr>
  <tr align="center">
    <td>
      <strong>fix_y = 0</strong>
    </td>
    <td>
      <strong>fix_y = 10</strong>
    </td>
  </tr>
  <tr>
    <td>
        <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/fix-y-0.webp"
        target="_blank">
          <img alt="fix-y-0"
          src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/fix-y-0.webp" />
        </a>
    </td>
    <td>
      <a href="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/fix-y-10.webp"
      target="_blank">
        <img alt="fix-y-10"
        src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/fix-y-10.webp" />
      </a>
    </td>
  </tr>
</table>

### Color

Within the `config.ini` file, you can customize the color of text and background in the overlay `labels`, as well as their opacity. The available options are as follows:

- `text_color`: Specifies the color of the text within the `labels`. You can use any of the color names from **CSS SVG Colors**. You can view a list of these colors [here](https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg).
<br />

- `background_color`: Defines the background color of the `labels` in the overlay. Similar to text_color, you can use any valid color name from **CSS SVG Colors**.
<br />

- `text_transparency`: Controls the opacity of the text within the `labels`.
<br />

- `background_transparency`: Controls the opacity of the background of the `labels`.

Adjust these values according to your preferences to customize the visual appearance of the overlay.

Remember to close and reopen the overlay after making changes in the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>text_color</td>
    <td>aquamarine</td>
    <td>string</td>
    <td>
        Must be a <a href="https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg">CSS SVG Color</a>
    </td>
  </tr>
  <tr align="center">
    <td>background_color</td>
    <td>darkslategray</td>
    <td>string</td>
    <td>
        Must be a <a href="https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg">CSS SVG Color</a>
    </td>
  </tr>
  <tr align="center">
    <td>text_transparency</td>
    <td>100</td>
    <td>integer</td>
    <td>Must be greater than or equal to 1 and less than or equal to 100</td>
  </tr>
  <tr align="center">
    <td>background_transparency</td>
    <td>60</td>
    <td>integer</td>
    <td>Must be greater than or equal to 1 and less than or equal to 100</td>
  </tr>
</table>

## Building - (For Developers)

```
$ git clone
```

```
$ python -m venv .venv
$ .venv\Scripts\activate
$ pip install .
$ build
```
You will find the `build` in the `build/dist` folder

## Python modules used

- PySide6 - v6.7.1
- cx_Freeze - last
- cursor - v1.3.5
- colorama - v0.4.6
- art - v6.2
- ahk[binary] - v1.7.4