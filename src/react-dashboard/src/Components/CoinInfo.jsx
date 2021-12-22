import { makeStyles } from '@material-ui/core';
import axios from 'axios';
import React, { useEffect } from 'react'
import { HistoricalChart } from '../config/api';
import { DashState } from '../DashContext';

const useStyles = makeStyles((theme) => ({

}))

const CoinInfo = ({ coin }) => {


    const classes = useStyles();
    const [historicalData, setHistoricalData] = React.useState([]);
    const [days, setDays] = React.useState([]);

    const { currency } = DashState();

    const fetchData = async () => {
        const { data } = await axios.get(HistoricalChart(coin.id, days, currency))
        setHistoricalData(data.prices);
    }
    useEffect(() => {
        fetchData();
    }, [currency, days])
    return (
        <div className={classes.container}>
            Coin Info
        </div>
    )
}

export default CoinInfo
