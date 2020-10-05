import Order from "./order";

export default function Orders({orders}) {
  return (

    <div className={'panel panel-inverse'} data-sortable-id="table-basic-7">
      <div className="panel-heading ui-sortable-handle">
        <h4 className="panel-title">Заказы </h4>
      </div>
      <div className="pannel-body">
        <div className="table-responsive">
          <table className="table m-b-0">
            <thead>
            <tr>
              <th>#</th>
              <th>Курьер</th>
              <th>Забрать</th>
              <th>Доставить</th>
              <th>Сумма Выкупа</th>
              <th>Статус</th>
            </tr>
            </thead>
            {
              !!orders && orders.length > 0 ?
            <tbody>
            {!!orders && orders.map((item, index) =>
              <Order order={item} index={index}/>
            )}

            </tbody>:
                <tbody>
                <td colspan='6' className='text-center'> Нихуя нет заказов за сегодня</td>
                </tbody>
            }
          </table>
        </div>
      </div>
    </div>
  )
}