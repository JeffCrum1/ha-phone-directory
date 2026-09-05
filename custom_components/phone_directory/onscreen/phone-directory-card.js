class PhoneDirectoryCard extends HTMLElement {
    constructor() {
        super();

        this.attachShadow({ mode: "open" });

        this._hass = null;
        this._config = {};
        this._contacts = [];
        this._loaded = false;
        this._dialog = null;
    }

    setConfig(config) {
        this._config = config || {};
    }

    set hass(hass) {
        this._hass = hass;

        if (!this._loaded) {
            this._loadContacts();
        }
    }

    get hass() {
        return this._hass;
    }

    async _loadContacts() {
        if (!this._hass) {
            return;
        }

        try {
            const result = await this._hass.connection.sendMessagePromise({
                type: "phone_directory/get_contacts",
            });

            this._contacts = result.contacts || [];
            this._loaded = true;

            this._renderContacts();
        } catch (error) {
            console.error("Phone Directory: failed to load contacts", error);
            this._renderError();
        }
    }

    _renderContacts() {
        const contacts = [...this._contacts].sort((a, b) =>
            a.name.localeCompare(b.name)
        );

        const rows = contacts
            .map(
                (contact) => `
          <div
            class="contact-row"
            data-contact-id="${this._escapeHtml(contact.contact_id)}"
          >
            <span class="contact-name">
              ${this._escapeHtml(contact.name)}
            </span>
            <span class="contact-number">
              ${this._escapeHtml(contact.number)}
            </span>
          </div>
        `
            )
            .join("");

        const emptyState =
            contacts.length === 0
                ? `
          <div class="empty-state">
            No contacts in the directory.
          </div>
        `
                : "";

        this.shadowRoot.innerHTML = `
      <ha-card>
        <div class="card-header">
          <div class="card-title">Phone Directory</div>
          <button class="add-button" id="add-contact">
            + Add Contact
          </button>
        </div>

        <div class="contacts">
          ${emptyState}
          ${rows}
        </div>
      </ha-card>

      <style>
        :host {
          display: block;
        }

        ha-card {
          overflow: hidden;
        }

        .card-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 16px;
        }

        .card-title {
          font-size: 24px;
          font-weight: 500;
        }

        .add-button {
          border: none;
          background: none;
          color: var(--primary-color);
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          padding: 8px;
          border-radius: 4px;
        }

        .add-button:hover {
          background: var(--secondary-background-color);
        }

        .contacts {
          padding: 0 16px 16px;
        }

        .contact-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          min-height: 48px;
          padding: 0 8px;
          border-top: 1px solid var(--divider-color);
          cursor: pointer;
          gap: 16px;
        }

        .contact-row:hover {
          background: var(--secondary-background-color);
        }

        .contact-name {
          font-weight: 500;
          min-width: 0;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        .contact-number {
          color: var(--secondary-text-color);
          white-space: nowrap;
        }

        .empty-state {
          padding: 16px 8px;
          color: var(--secondary-text-color);
        }

        .dialog-backdrop {
          position: fixed;
          inset: 0;
          z-index: 1000;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(0, 0, 0, 0.4);
        }

        .dialog {
          width: min(420px, calc(100vw - 32px));
          background: var(--card-background-color);
          color: var(--primary-text-color);
          border-radius: 12px;
          box-shadow: var(--ha-box-shadow, 0 4px 20px rgba(0, 0, 0, 0.3));
          padding: 24px;
          box-sizing: border-box;
        }

        .dialog-title {
          font-size: 20px;
          font-weight: 500;
          margin-bottom: 20px;
        }

        .field {
          margin-bottom: 16px;
        }

        .field label {
          display: block;
          font-size: 14px;
          color: var(--secondary-text-color);
          margin-bottom: 6px;
        }

        .field input {
          width: 100%;
          box-sizing: border-box;
          padding: 10px 12px;
          border: 1px solid var(--divider-color);
          border-radius: 4px;
          background: var(--primary-background-color);
          color: var(--primary-text-color);
          font-size: 16px;
        }

        .field input:focus {
          outline: 2px solid var(--primary-color);
          outline-offset: -1px;
        }

        .dialog-actions {
          display: flex;
          justify-content: flex-end;
          gap: 8px;
          margin-top: 24px;
        }

        .dialog-actions button {
          border: none;
          background: none;
          color: var(--primary-color);
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          padding: 10px 16px;
          border-radius: 4px;
        }

        .dialog-actions button:hover {
          background: var(--secondary-background-color);
        }

        .dialog-actions .delete-button {
          margin-right: auto;
          color: var(--error-color);
        }

        .confirmation-text {
          color: var(--secondary-text-color);
          line-height: 1.5;
        }

        .error-message {
          color: var(--error-color);
          margin-top: 8px;
          font-size: 14px;
          line-height: 1.4;
        }
      </style>
    `;

        this.shadowRoot
            .querySelector("#add-contact")
            ?.addEventListener("click", () => {
                this._openAddDialog();
            });

        this.shadowRoot.querySelectorAll(".contact-row").forEach((row) => {
            row.addEventListener("click", () => {
                this._openEditDialog(row.dataset.contactId);
            });
        });
    }

    _renderError() {
        this.shadowRoot.innerHTML = `
      <ha-card>
        <div class="card-header">
          <div class="card-title">Phone Directory</div>
        </div>
        <div class="contacts">
          <div class="empty-state">
            Unable to load the phone directory.
          </div>
        </div>
      </ha-card>
    `;
    }

    _openAddDialog() {
        this._closeDialog();

        const backdrop = document.createElement("div");
        backdrop.className = "dialog-backdrop";

        backdrop.innerHTML = `
      <div class="dialog">
        <div class="dialog-title">Add Contact</div>

        <div class="field">
          <label for="contact-name">Name</label>
          <input
            id="contact-name"
            type="text"
            autocomplete="off"
          />
        </div>

        <div class="field">
          <label for="contact-number">Number</label>
          <input
            id="contact-number"
            type="tel"
            autocomplete="off"
          />
        </div>

        <div class="error-message" id="dialog-error" hidden></div>

        <div class="dialog-actions">
          <button id="cancel">Cancel</button>
          <button id="save">Save</button>
        </div>
      </div>
    `;

        this.shadowRoot.appendChild(backdrop);
        this._dialog = backdrop;

        backdrop.querySelector("#cancel").addEventListener("click", () => {
            this._closeDialog();
        });

        backdrop.querySelector("#save").addEventListener("click", async () => {
            await this._saveNewContact();
        });

        backdrop.addEventListener("click", (event) => {
            if (event.target === backdrop) {
                this._closeDialog();
            }
        });

        const nameInput = backdrop.querySelector("#contact-name");
        nameInput.focus();
    }

    async _saveNewContact() {
        const nameInput = this._dialog.querySelector("#contact-name");
        const numberInput = this._dialog.querySelector("#contact-number");
        const errorElement = this._dialog.querySelector("#dialog-error");

        const name = nameInput.value.trim();
        const number = numberInput.value.trim();

        errorElement.hidden = true;

        if (!name || !number) {
            errorElement.textContent = "Name and number are required.";
            errorElement.hidden = false;
            return;
        }

        try {
            await this._hass.callService(
                "phone_directory",
                "add_contact",
                {
                    name,
                    number,
                }
            );

            this._closeDialog();

            this._loaded = false;
            await this._loadContacts();
        } catch (error) {
            console.error("Phone Directory: failed to add contact", error);

            errorElement.textContent = this._getServiceErrorMessage(error);
            errorElement.hidden = false;
        }
    }

    _openEditDialog(contactId) {
        const contact = this._contacts.find(
            (item) => item.contact_id === contactId
        );

        if (!contact) {
            return;
        }

        this._closeDialog();

        const backdrop = document.createElement("div");
        backdrop.className = "dialog-backdrop";

        backdrop.innerHTML = `
      <div class="dialog">
        <div class="dialog-title">Edit Contact</div>

        <div class="field">
          <label for="contact-name">Name</label>
          <input
            id="contact-name"
            type="text"
            value="${this._escapeHtml(contact.name)}"
            autocomplete="off"
          />
        </div>

        <div class="field">
          <label for="contact-number">Number</label>
          <input
            id="contact-number"
            type="tel"
            value="${this._escapeHtml(contact.number)}"
            autocomplete="off"
          />
        </div>

        <div class="error-message" id="dialog-error" hidden></div>

        <div class="dialog-actions">
          <button class="delete-button" id="delete">Delete</button>
          <button id="cancel">Cancel</button>
          <button id="save">Save</button>
        </div>
      </div>
    `;

        this.shadowRoot.appendChild(backdrop);
        this._dialog = backdrop;

        backdrop.querySelector("#cancel").addEventListener("click", () => {
            this._closeDialog();
        });

        backdrop.querySelector("#save").addEventListener("click", async () => {
            await this._saveContact(contactId);
        });

        backdrop.querySelector("#delete").addEventListener("click", () => {
            this._openDeleteConfirmation(contactId);
        });

        backdrop.addEventListener("click", (event) => {
            if (event.target === backdrop) {
                this._closeDialog();
            }
        });

        backdrop.querySelector("#contact-name").focus();
    }

    async _saveContact(contactId) {
        const nameInput = this._dialog.querySelector("#contact-name");
        const numberInput = this._dialog.querySelector("#contact-number");
        const errorElement = this._dialog.querySelector("#dialog-error");

        const name = nameInput.value.trim();
        const number = numberInput.value.trim();

        errorElement.hidden = true;

        if (!name || !number) {
            errorElement.textContent = "Name and number are required.";
            errorElement.hidden = false;
            return;
        }

        try {
            await this._hass.callService(
                "phone_directory",
                "change_contact",
                {
                    contact_id: contactId,
                    name,
                    number,
                }
            );

            this._closeDialog();

            this._loaded = false;
            await this._loadContacts();
        } catch (error) {
            console.error("Phone Directory: failed to save contact", error);

            errorElement.textContent = this._getServiceErrorMessage(error);
            errorElement.hidden = false;
        }
    }

    _openDeleteConfirmation(contactId) {
        const contact = this._contacts.find(
            (item) => item.contact_id === contactId
        );

        if (!contact) {
            return;
        }

        this._closeDialog();

        const backdrop = document.createElement("div");
        backdrop.className = "dialog-backdrop";

        backdrop.innerHTML = `
      <div class="dialog">
        <div class="dialog-title">Delete Contact</div>

        <div class="confirmation-text">
          Are you sure you want to delete
          <strong>${this._escapeHtml(contact.name)}</strong>?
        </div>

        <div class="dialog-actions">
          <button id="cancel">Cancel</button>
          <button id="confirm-delete">Delete</button>
        </div>
      </div>
    `;

        this.shadowRoot.appendChild(backdrop);
        this._dialog = backdrop;

        backdrop.querySelector("#cancel").addEventListener("click", () => {
            this._closeDialog();
            this._openEditDialog(contactId);
        });

        backdrop
            .querySelector("#confirm-delete")
            .addEventListener("click", async () => {
                await this._deleteContact(contactId);
            });

        backdrop.addEventListener("click", (event) => {
            if (event.target === backdrop) {
                this._closeDialog();
                this._openEditDialog(contactId);
            }
        });
    }

    async _deleteContact(contactId) {
        try {
            await this._hass.callService(
                "phone_directory",
                "delete_contact",
                {
                    contact_id: contactId,
                }
            );

            this._closeDialog();

            this._loaded = false;
            await this._loadContacts();
        } catch (error) {
            console.error("Phone Directory: failed to delete contact", error);
        }
    }

    _getServiceErrorMessage(error) {
        if (error?.message) {
            return error.message.replace(/^Validation error:\s*/i, "");
        }

        return "Unable to complete the operation.";
    }

    _closeDialog() {
        if (this._dialog) {
            this._dialog.remove();
            this._dialog = null;
        }
    }

    _escapeHtml(value) {
        const element = document.createElement("div");
        element.textContent = value;
        return element.innerHTML;
    }
}

customElements.define("phone-directory-card", PhoneDirectoryCard);
