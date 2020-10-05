import classNames from 'classnames';

export default function Courier ({courier, index}) {

  const style = classNames({
      color: setStatusColor(),
    });

  function setStatusColor() {
    if (courier.order_status === 'accepted') {
      return 'blue'
    }
    if (courier.order_status === 'in_progress') {
      return 'yellow'
    }
    if (courier.order_status === 'done') {
      return 'green'
    }
    if (courier.order_status === 'cancel') {
      return 'red'
    }
  }

  return (
    <tr key={index}>
      <td>{courier.courier.first_name}</td>
      <td>{courier.courier.phone_number}</td>
      <td>{courier.courier.delivery_type}</td>
      <td>{courier.courier.vehicle}</td>
      <td><small>{courier.start_time}</small></td>
      <td style={{ 'backgroundColor': setStatusColor()}}>{courier.order_status}</td>
    </tr>
  )
}