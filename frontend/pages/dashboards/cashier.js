import Layout from "../../components/layout";
import Main from "../../components/main";
import {useEffect} from "react";
import {fetchCouriersFromServer} from "../../lib/data_fetch";
import Couriers from "../../components/couriers";
import couriers from "../../components/couriers";


class CashierDashboard extends React.Component {
  state = {
    couriers: []
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

  fetchCouriers() {
    this.interval = setInterval(() => {
      fetchCouriersFromServer(this.state.date).then((data) => {
        this.setState({
          couriers: data
        })
      })
    }, 5000)
  }

  componentDidMount() {
    this.fetchCouriers()
  }

  // componentWillUnmount() {
  //   clearInterval(this.interval)
  // }

  render() {
    const {couriers} = this.state;

    return (
      <Layout>
        <Main>
          <h1>Cashier dashboard</h1>
          <Couriers couriers={couriers}/>
        </Main>
      </Layout>
    )
  }
}

export default CashierDashboard