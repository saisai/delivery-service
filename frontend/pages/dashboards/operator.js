import Main from "../../components/main";
import Layout from "../../components/layout";
import {
  getAllDataFromServer,
  fetchCouriersFromServer,
  fetchOrdersFromServer,
  checkOperatorShift
} from "../../lib/data_fetch";
import Couriers from "../../components/couriers";
import Orders from "../../components/orders";
import NewOrder from "../../components/newOrder";
import React from "react";
import StartEndShiftModal from "../../components/working-shift/operatorWorkingShift";


class Operator extends React.Component {
  state = {
    streets: [],
    districts: [],
    cities: [],
    addresses: [],
    orders: [],
    date: this.formatDate(new Date()),
    errors: [],
    operator: {
      start_time: null
    },
    isLoading: true,
  }

  formatDate(date) {
    var d = new Date(date),
      month = '' + (d.getMonth() + 1),
      day = '' + d.getDate(),
      year = d.getFullYear();

    if (month.length < 2)
      month = '0' + month;
    if (day.length < 2)
      day = '0' + day;

    return [year, month, day].join('-');
  }

  fetchOrders() {
    this.ordersInterval = setInterval(() => {
      fetchOrdersFromServer(this.state.date).then((data) => {
        this.setState({orders: data})
      })
    }, 5000)
  }

  fetchCouriers() {
    this.couriersInterval = setInterval(() => {
      fetchCouriersFromServer(this.state.date).then((data) => {
        this.setState({
          couriers: data
        })
      })
    }, 5000)
  }

  checkOperator() {
    this.operatorInterval = setInterval(() => {
      checkOperatorShift(this.state.date).then((data) => {
        console.log(data)
        if (data['non_field_errors']) {
          this.setState({
            errors: data['non_field_errors'],
            isLoading: false,
          })
          // clearInterval(this.couriersInterval);
          // clearInterval(this.operatorInterval);
          // clearInterval(this.operatorInterval);
        }

        if (data.length > 0) {
          if (this.state.operator !== data[0]) {
            this.setState({
              operator: data[0],
              isLoading: false
            })
            console.log("SETIT")

          }
        }
        if (data.length === 0) {
          this.setState({isLoading: false})
        }

      })
    }, 5000)
  }

  componentDidMount() {
    getAllDataFromServer().then((data) => {
      this.setState({
        cities: data.cities,
        districts: data.districts,
        streets: data.streets,
      })
    })
    this.fetchCouriers();
    this.fetchOrders();
    this.checkOperator();
  }

  componentWillUnmount() {
    clearInterval(this.ordersInterval);
    clearInterval(this.couriersInterval);
  }

  startShift() {
    console.log("startShift")
  }

  endShift() {
    console.log("endShift")
  }

  clearErrors = () => {
    this.setState({
      errors: []
    })
  }

  setOperatorShift = (data) => {
    this.setState({
      operator: data
    })
  }

  render() {
    const {
      cities,
      districts,
      streets,
      couriers,
      orders,
      errors,
      operator,
      isLoading,
    } = this.state;

    console.log(operator.start_time)
    console.log(errors)
    console.log(errors.length === 0 && operator.start_time !== null)

    return (
      <Layout>
        {isLoading ?
          <div>Loading...</div>
          :
          <>
            {errors.length === 0 && operator.start_time !== null?
              <Main>
                <h1 className='page-header mb-3'>Панель оператора</h1>
                <div className="d-sm-flex align-items-center m-b-10">
                  <div className='col-xl-5'>
                    <NewOrder
                      cities={cities}
                      districts={districts}
                      streets={streets}
                      couriers={couriers}
                    />
                  </div>


                </div>
                <div className='row'>
                  <div className='col-xl-8'>
                    <Orders orders={orders}/>
                  </div>
                  <div className='col-xl-4 ui-sortable'>
                    <Couriers couriers={couriers}/>
                  </div>
                </div>
              </Main> :
              <StartEndShiftModal
                startShift={this.startShift}
                endShift={this.endShift}
                errors={errors}
                clearErrors={this.clearErrors}
                operator={operator}
                setOperatorShift={this.setOperatorShift}
              />
            }
          </>
        }

      </Layout>
    )
  }
}

export default Operator