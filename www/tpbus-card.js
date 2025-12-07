class TPBusCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('Please define an entity');
    }
    this.config = config;
  }

  set hass(hass) {
    const entityId = this.config.entity;
    const state = hass.states[entityId];

    if (!state) {
      this.shadowRoot.innerHTML = `
        <ha-card>
          <div class="card-content">Entity not found: ${entityId}</div>
        </ha-card>
      `;
      return;
    }

    const attributes = state.attributes;
    const arrivalTime = state.state;
    const isAvailable = arrivalTime !== "unavailable";
    const updateTime = attributes.update_time;
    const timeAgo = updateTime ? this._getTimeAgo(updateTime) : null;

    this.shadowRoot.innerHTML = `
      <style>
        .card-content {
          padding: 16px;
        }
        .bus-card {
          font-family: var(--paper-font-body1_-_font-family);
        }
        .header {
          display: flex;
          align-items: center;
          margin-bottom: 16px;
        }
        .header ha-icon {
          margin-right: 8px;
          color: var(--primary-color);
        }
        .title {
          font-size: 24px;
          font-weight: 500;
          color: var(--primary-text-color);
        }
        .info-row {
          display: flex;
          justify-content: space-between;
          padding: 8px 0;
          border-bottom: 1px solid var(--divider-color);
        }
        .info-row:last-child {
          border-bottom: none;
        }
        .label {
          color: var(--secondary-text-color);
          font-weight: 500;
        }
        .value {
          color: var(--primary-text-color);
          text-align: right;
          max-width: 60%;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .update-time {
          margin-top: 16px;
          padding-top: 8px;
          border-top: 1px solid var(--divider-color);
          color: var(--secondary-text-color);
          font-size: 12px;
          text-align: center;
        }
        .status-badge {
          display: inline-block;
          padding: 4px 12px;
          border-radius: 12px;
          background-color: var(--primary-color);
          color: white;
          font-size: 12px;
          font-weight: 500;
        }
        .arrival-time {
          font-size: 32px;
          font-weight: bold;
          text-align: center;
          padding: 16px 0;
          color: var(--primary-color);
        }
        .unavailable {
          color: var(--error-color);
        }
      </style>
      <ha-card>
        <div class="card-content bus-card">
          <div class="header">
            <ha-icon icon="mdi:bus-stop"></ha-icon>
            <div class="title">${this.config.title || 'Bus Stop'}</div>
          </div>
          
          <div class="arrival-time ${!isAvailable ? 'unavailable' : ''}">
            ${isAvailable ? this._formatArrivalTime(arrivalTime) : 'N/A'}
          </div>
          
          ${timeAgo ? `
            <div class="update-time">
              Updated ${timeAgo}
            </div>
          ` : ''}
        </div>
      </ha-card>
    `;
  }

  _getStatusText(status) {
    const statusMap = {
      '0': 'Inactive',
      '1': 'Active',
      '2': 'Approaching',
    };
    return statusMap[status] || `Status ${status}`;
  }

  getCardSize() {
    return 2;
  }

  _formatArrivalTime(seconds) {
    const sec = parseInt(seconds);
    if (isNaN(sec)) return seconds + 's';
    
    const minutes = Math.floor(sec / 60);
    const remainingSeconds = sec % 60;
    
    if (minutes > 0) {
      return `${minutes}m ${remainingSeconds}s`;
    }
    return `${sec}s`;
  }

customElements.define('tpbus-card', TPBusCard);
  _formatArrivalTime(seconds) {
    const sec = parseInt(seconds);
    if (isNaN(sec)) return seconds + 's';
    
    const minutes = Math.floor(sec / 60);
    const remainingSeconds = sec % 60;
    
    if (minutes > 0) {
      return `${minutes}m ${remainingSeconds}s`;
    }
    return `${sec}s`;
  }

  _getTimeAgo(updateTimeStr) {
    try {
      // Parse format like "2025-12-07 10:17:49"
      const updateTime = new Date(updateTimeStr.replace(' ', 'T'));
      const now = new Date();
      const diffMs = now - updateTime;
      const diffMinutes = Math.floor(diffMs / 60000);
      
      if (diffMinutes < 1) {
        return 'less than 1 minute ago';
      } else if (diffMinutes === 1) {
        return '1 minute ago';
      } else {
        return `${diffMinutes} minutes ago`;
      }
    } catch (e) {
      return updateTimeStr;
    }
  }