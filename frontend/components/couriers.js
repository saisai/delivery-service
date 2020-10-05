import Courier from "./courier";


export default function Couriers({couriers}) {

  return (
    <div className={'panel panel-inverse'} data-sortable-id="table-basic-7">
      <div className="panel-heading ui-sortable-handle">
        <h4 className="panel-title">Курьеры </h4>
      </div>
      <div className="pannel-body">
        <div className="table-responsive">
          <table className='table table-striped m-b-0'>
            <thead>
            <tr>
              <th>Имя</th>
              <th>номер Телефона</th>
              <th>Тип курьера</th>
              <th>Т/С</th>
              <th>Время начала смены</th>
              <th>Наличие заказа</th>
            </tr>
            </thead>

            { couriers.length > 0 ?
              <tbody>
            {!!couriers && couriers.map((item, index) =>
              <Courier courier={item} index={index}/>
            )}
            </tbody>
            :
              <tbody>
                <td colspan='6' className='text-center'>Нихуя нет активных курьеров</td>
              </tbody>
            }
          </table>
        </div>
      </div>
    </div>
  )
}