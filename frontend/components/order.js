import classNames from 'classnames';

export default function Order ({order, index}) {

  function setStatusColor() {
    if (order.status === 'accepted') {
      return 'table-info'
    }
    if (order.status === 'in_progress') {
      return 'table-active'
    }
    if (order.status === 'done') {
      return 'table-success'
    }
    if (order.status === 'cancel') {
      return 'table-danger'
    }
  }

  return (
    <tr key={index}>
      <td className={setStatusColor()}>{order.id}</td>
      <td className={setStatusColor()}>{order.courier_shift.courier_name}</td>
      <td className={setStatusColor()}>{order.delivery_from.district.name} - {order.delivery_from.street.name}</td>
      <td className={setStatusColor()}>{order.delivery_to.district.name} - {order.delivery_to.street.name}</td>
      <td className={setStatusColor()}>{order.ransom_sum} сом </td>
      <td className={setStatusColor()}>{order.status}</td>
    </tr>
  )
}