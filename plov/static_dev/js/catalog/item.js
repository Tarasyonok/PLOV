document.addEventListener('DOMContentLoaded', () => {
    const ratingForm = document.querySelector('.rating-form');
    const stars = document.querySelectorAll('.star');
    const starLabels = document.querySelectorAll('.star-label');

    starLabels.forEach(label => {
      const labelStar = label.querySelector('.star');
      const svgPath = label.querySelector('.star-shape svg path');
      if (labelStar.value <= ratingForm.rating.value) {
        svgPath.classList.remove('star-not-active');
        svgPath.classList.add('star-active');
      } else {
        svgPath.classList.remove('star-active');
        svgPath.classList.add('star-not-active');
      }
    });

    stars.forEach(star => {
      star.addEventListener('change', () => {
        const selectedValue = star.value;
        starLabels.forEach(label => {
          const labelStar = label.querySelector('.star');
          const svgPath = label.querySelector('.star-shape svg path');
          if (labelStar.value <= selectedValue) {
            svgPath.classList.remove('star-not-active');
            svgPath.classList.add('star-active');
          } else {
            svgPath.classList.remove('star-active');
            svgPath.classList.add('star-not-active');
          }
        });
        ratingForm.rating.value = selectedValue;
        ratingForm.submit();
      });
    });
  });
