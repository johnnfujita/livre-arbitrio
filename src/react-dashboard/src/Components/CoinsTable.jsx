import React, { useEffect } from 'react'
import { CoinList } from '../config/api'
import { DashState } from '../DashContext'
import axios from "axios";
import { Container, Typography, TextField, LinearProgress, TableContainer, Table, TableHead, TableRow, TableCell, TableBody } from '@material-ui/core';
import { useNavigate } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import { Pagination } from '@material-ui/lab';
const useStyles = makeStyles({
    row: {
        backgroundColor: "#16171a",
        cursor: "pointer",
        "&:hover": {
            backgroundColor: "#131111",
        },
        fontFamily: "Roboto"
    },
    pagination: {
        "& .MuiPaginationItem-root": {
            color: "aqua"
        }
    }

});

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
const CoinsTable = () => {
    const [coins, setCoins] = React.useState([]);
    const [isLoading, setIsLoading] = React.useState(true);
    const [search, setSearch] = React.useState('');
    const [page, setPage] = React.useState(1);

    const classes = useStyles();
    const navigate = useNavigate();
    const { currency, symbol } = DashState();

    const fetchData = async () => {
        setIsLoading(true);
        const { data } = await axios.get(CoinList(currency));
        setCoins(data);

        setIsLoading(false);

    }

    const handleSearch = () => {
        return coins.filter(
            (coin) => coin.name.toLowerCase().includes(search.toLowerCase()) || coin.symbol.toLowerCase().includes(search.toLowerCase()))
    }

    useEffect(() => {
        fetchData();
        console.log(coins)
    }, [currency])

    return (
        <Container style={{ textAlign: "center" }}>
            <Typography variant="h4" style={{ margin: 18, fontFamily: "Roboto" }}>
                Crypto List
            </Typography>
            <TextField label="Search" value={search} variant="outlined" style={{ marginBottom: 20, width: "100%" }} onChange={e => setSearch(e.target.value)} />
            <TableContainer>
                {isLoading ? (
                    <LinearProgress style={{ backgroundColor: "aqua" }} />) :
                    (
                        <Table>
                            <TableHead style={{ backgroundColor: "aqua", borderRadius: "8px" }}>
                                <TableRow>
                                    {["Coin", "Price", "24h Change", "Market Cap"].map((head) => (
                                        <TableCell style={{ color: "black", fontWeight: "700", fontFamily: "Roboto", }}
                                            key={head}
                                            align={head === "Coin" ? "" : "right"}
                                        >
                                            {head}

                                        </TableCell>
                                    ))}
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {handleSearch()
                                    .slice((page - 1) * 10, page * 10)
                                    .map((row) => {
                                        return (
                                            <TableRow
                                                onClick={() => navigate(`/symbols/${row.id}`)}
                                                className={classes.row}
                                                key={row.name}

                                            >
                                                <TableCell
                                                    component="th"
                                                    scope="row"
                                                    style={{
                                                        display: "flex",

                                                        gap: 15
                                                    }}
                                                >

                                                    <img src={row?.image} alt={row?.name} height="50px" style={{ marginBottom: 10, }} />
                                                    <div style={{ display: "flex", flexDirection: "column" }}>
                                                        <span
                                                            style={{ textTransform: "uppercase", fontSize: 22 }}
                                                        >{row.symbol}</span>
                                                        <span style={{ color: "darkgrey" }}>{row.name}</span>

                                                    </div>
                                                </TableCell>
                                                <TableCell align="right">
                                                    {symbol}{" "}
                                                    {numberWithCommas(row.current_price.toFixed(2))}
                                                </TableCell>
                                                <TableCell
                                                    align="right"
                                                    style={{ color: row.price_percentage_change_24h > 0 ? "green" : "red", fontWeight: 500 }}
                                                >
                                                    {row.price_change_percentage_24h.toFixed(2)}%

                                                </TableCell>
                                                <TableCell
                                                    align="right"

                                                >
                                                    {symbol}{" "}{numberWithCommas(row.market_cap.toString().slice(0, - 6))}

                                                </TableCell>
                                            </TableRow>
                                        )
                                    })}
                            </TableBody>
                        </Table>)
                }
            </TableContainer>
            <Pagination
                number={(handleSearch()?.length / 10).toFixed(0)}
                style={{
                    padding: 20,
                    width: "100%",
                    display: "flex",
                    justifyContent: "center",
                }}
                classes={{ ul: classes.pagination }}
            />
        </Container>
    )
}

export default CoinsTable
