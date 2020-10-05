export function redirectToAppropriateDashboard() {
  const DASHBOARD_NAMES_HASH = {
    'CAN_VIEW_CASHIER_TAB': 'cashier',
    'CAN_VIEW_COURIER_TAB': 'courier',
    'CAN_VIEW_OPERATOR_TAB': 'operator',
  }
  const localRole = localStorage.getItem('permissions')
  if (localRole) {
    window.location.href = `/dashboards/${DASHBOARD_NAMES_HASH[localRole]}`
  } else {
    window.location.href = `/auth/login`
  }
}

