import './App.css';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import Slider from "react-slick";
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import React, { useState, useEffect } from 'react';
import axios from 'axios';


function App() {
  const [data, setData] = useState('');

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/') 
            .then(response => {
                setData(response.data.message);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }, []);
  var settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
  };
  return (
        <Slider {...settings}>
      <Card>
        <CardContent>
          iuvesauidoshebvyoueinrfvsgoebwoyrgoesnruvyye
        </CardContent>
      </Card>
      <Card>
        <CardContent>
          iuvesauidoshebvyoueinrfvsgoebwoyrgoesnruvyye
        </CardContent>
      </Card>
    </Slider>
  );
}

export default App;
