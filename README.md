# Phone Directory

A Home Assistant custom integration for managing a household phone directory.

## Why?

The phone system in our house is primarily an **emergency backup**.

If a cell phone stops working, there should still be a simple way for someone at home to call family. The system uses VoIP.ms for telephone service and Grandstream handsets for the physical phones.

Both systems need a phonebook.

Rather than maintaining those phonebooks separately, Phone Directory keeps **one directory in Home Assistant** and provides the information to the systems that need it.

Add a contact once. Change it once. Delete it once.

Home Assistant remains the place where the directory is maintained.

## How It Works

Phone Directory manages the directory inside Home Assistant.

It uses **Comlink** to connect that directory with the systems that use it. Each system can have its own way of receiving the directory, while Phone Directory remains the single place where contacts are maintained.

Currently, Phone Directory supports:

* **Grandstream**
* **VoIP.ms**

If you use those systems, you're ready to go.

If you have different hardware or a different service and want to connect it to Phone Directory, the project is designed to be extended. See the [Comlink documentation](custom_components/phone_directory/comlink/README.md) for more information.

# Installation

## HACS — Recommended

Phone Directory can be installed through [HACS](https://hacs.xyz/).

Because Phone Directory is currently distributed as a custom integration, the repository needs to be added to HACS as a custom repository.

1. Open **HACS** in Home Assistant.

2. Select **Integrations**.

3. Open the **⋮** menu in the upper-right corner.

4. Select **Custom repositories**.

5. Enter:

   ```text
   https://github.com/JeffCrum1/ha-phone-directory
   ```

6. Select **Integration** as the category.

7. Select **Add**.

8. Find **Phone Directory** in HACS.

9. Select **Download**.

10. Restart Home Assistant.

Once Home Assistant has restarted, add Phone Directory from:

**Settings → Devices & services → Add Integration**

Search for **Phone Directory** and follow the configuration flow.

## Manual Installation

Phone Directory can also be installed without HACS.

1. Download or clone this repository.

2. Copy the entire:

   ```text
   custom_components/phone_directory
   ```

   directory into:

   ```text
   /config/custom_components/phone_directory
   ```

3. Restart Home Assistant.

Once Home Assistant has restarted, add Phone Directory from:

**Settings → Devices & services → Add Integration**

Search for **Phone Directory** and follow the configuration flow.

## Configuration

Phone Directory is designed as a **single-instance integration**.

After adding the integration, its configuration is managed through the Home Assistant integration options. Add and configure the outputs you need, then maintain your contacts from Home Assistant.

---

If you have Grandstream and VoIP.ms, that's all you need to know to get started.

If you're looking at Phone Directory and thinking, **“Oooo... I could use this with my hardware/service,”** that's where the deeper Comlink documentation comes in.

## Where It Started

We started this with:

> *“Maybe a couple scripts that read a helper and send some data out.”*

It turned into something considerably more useful.

And that's a good thing.
