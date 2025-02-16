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
        axios.get("http://127.0.0.1:8000/")
            .then(response => {console.log(response.data);setData(response.data)})
            .catch(error => console.error("Error:", error));
    }, []);
  var settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
  };
  const cardCount=[];
  for(let i=0;i<data.length;i++){
    cardCount.push(
      <Card key={i}>
        <CardContent>
          {data[i].content}
        </CardContent>
      </Card>
    )
  }
  return (
    <Slider {...settings}>
      {cardCount}
    </Slider>
  );
}

export default App;
