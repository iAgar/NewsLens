import './App.css';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import Slider from "react-slick";
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';


function App() {
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
