/**
 * Created by johnsmac on 19/1/2017.
 */
// var AUD = {
//     player: $("#audio_controller")[0],
//     division_player: $('#player'),
//
//     init: function () {
//         AUD.player.volume = 0.1;
//
//         $("#play_song_button").on("click", function () {
//             console.log('===============click button==============')
//             AUD.division_player.style.display = 'block'
//             AUD.player.src = $("#play_song_button_a").val();
//             if (AUD.player.paused) {
//                 AUD.player.play();
//             }
//         });
//
//         AUD.player.addEventListener("ended", function () {
//             if (AUD.player.playing) {
//                 AUD.player.stop()
//                 AUD.division_player.style.display = 'none'
//             }
//         });
//
//     },
//
// };
// $(document).ready(function () {
//     AUD.init();
// });