// ------------------------------------------------------------------------------------------------------------
//How this Function works:
//
// This creates a clickable thumbnails of images on AGgrid table

//--------------------------------------------------------------------------------------------------------------

dagcomponentfuncs.ImgThumbnail = function (props) {
            const {setData, data} = props;
            
            
            //console.log("Hellllllllllllooooo")
            //console.log(`${data.image_link}`)
            //console.log(`${data.media_link}`)
            
            
            function onClick() {
                // Construct the video URL using the media server's base URL and the media link
                const videoUrl = `${data.media_link}`;               
                console.log(videoUrl)
                setData({ value: videoUrl, image_link: data.image_link });
            }
            
            //Creating and styling thumbnail div
            return React.createElement(
                'div',
                {
                    style: {
                        width: '100%',
                        //height: '100%',
                        display: 'flex',
                        alignItems: 'center',
                    },
                },
                React.createElement(
                    'img',
                    {
                        onClick,
                        style: {width: '100%', height: 'auto'},
                        src: `${data.image_link}`,
        
                    },
                )
            );
};
   
    
    
    
    