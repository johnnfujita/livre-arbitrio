import axios from 'axios'
import React, { useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { SingleCoin } from '../config/api'
import { DashState } from '../DashContext';
import { LinearProgress, makeStyles, Typography } from '@material-ui/core';
import CoinInfo from '../Components/CoinInfo';
import parse from 'html-react-parser';


function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

const useStyles = makeStyles((theme) => ({
    container: {
        display: 'flex',
        [theme.breakpoints.down("md")]: {
            flexDirection: 'column',
            alignItems: 'center',
        }
    },
    sidebar: {
        width: "30%",
        [theme.breakpoints.down('md')]: {
            width: '100%'
        },
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        marginTop: 25,
        borderRight: '1px solid rgba(255,255,255,.1)',
    },
    heading: {
        fontWeight: "bold",
        marginBottom: 20,
        fontFamily: 'Roboto'
    },
    description: {
        width: "100%",
        fontFamily: "Roboto",
        padding: 25,
        paddingBottom: 15,
        paddingTop: 0,
        textAlign: "justify"
    },
    marketData: {
        alignSelf: "start",
        padding: 25,
        paddingTop: 10,
        width: "100%",
        [theme.breakpoints.down("md")]: {
            display: "flex",
            justifyContent: "space-around"
        },
        [theme.breakpoints.down("sm")]: {
            flexDirection: "column",
            alignItems: "center"
        },
        [theme.breakpoints.down("xs")]: {
            alignItems: "start"
        }
    }

}));

const SymbolDetail = () => {

    const classes = useStyles();

    const params = useParams()
    const [coin, setCoin] = React.useState()

    const { currency, symbol } = DashState();

    console.log(params)
    const fetchData = async () => {
        const { data } = await axios.get(SingleCoin(params.symbol))
        setCoin(data);

    };

    useEffect(() => {
        fetchData();

    }, [currency])

    if (!coin) return <LinearProgress style={{ backgroundColor: "aqua" }} />
    return (
        <div className={classes.container}>
            <div className={classes.sidebar}>
                <img src={coin?.image.large} alt={coin?.name} height={200} style={{ marginBottom: 20 }} />
                <Typography
                    variant="h3"
                    className={classes.heading}
                >
                    {coin?.name}
                </Typography>
                <Typography variant="subtitle1" className={classes.description}>
                    {parse(`${coin?.description.en.split(". ")[0]}`)}
                </Typography>
                <div className={classes.marketData}>
                    <span style={{ display: "flex" }}>
                        <Typography variant="h5" className={classes.heading}>
                            Rank:
                        </Typography>
                        &nbsp;&nbsp;
                        <Typography variant="h5" style={{ fontFamily: "Roboto" }}>
                            {coin?.market_cap_rank}
                        </Typography>
                    </span>
                    <span style={{ display: "flex" }}>
                        <Typography variant="h5" className={classes.heading}>
                            Current Price:
                        </Typography>
                        &nbsp;&nbsp;
                        <Typography variant="h5" style={{ fontFamily: "Roboto" }}>
                            {symbol}{" "}{numberWithCommas(coin?.market_data.current_price[currency.toLowerCase()])}
                        </Typography>
                    </span>
                    <span style={{ display: "flex" }}>
                        <Typography variant="h5" className={classes.heading}>
                            Market Cap:
                        </Typography>
                        &nbsp;&nbsp;
                        <Typography variant="h5" style={{ fontFamily: "Roboto" }}>
                            {symbol}{" "}{numberWithCommas(coin?.market_data.market_cap[currency.toLowerCase()]
                                .toString()
                                .slice(0, -6)
                            )}M
                        </Typography>
                    </span>
                </div>
            </div>
            <CoinInfo coin={coin} />
        </div>
    )
}

export default SymbolDetail
